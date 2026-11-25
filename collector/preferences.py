"""사용자 관심도: 순위표(rank.py) 점수에 더하는 가산·감산과 탐색 몫. 핵심 계산은 taste.py, 이 파일은 이 프로젝트와의 연결.

세 가지를 쓴다.
1. 직접 지정 (collector/interests.json): "더 보고 싶은 것 / 덜 보고 싶은 것"으로 적은 분야·출처·낱말. 항목마다 +2 / -3.
2. 내용 유사도 (taste.py): 사이트 주인의 반응과 읽은 기록이 붙은 글을 라벨로 삼아, 새 후보가 좋아한 글과 닮았으면 +,
   싫어한 글과 닮았으면 -. -4 ~ +4.
   신호는 사이트(web/src/lib/signals.ts)가 비공개 저장소 ai-brief-transcripts의 signals/ 아래 JSON 파일로 올린다.
   글쓰기 작업이 이 저장소를 옆 폴더에 받아 두므로 여기서는 파일만 읽는다. 공개 저장소(data/)로 옮기지 않는다.
3. 탐색 몫: 취향에 갇히지 않도록, 화제성은 높은데 아직 반응이 거의 없는 영역의 후보를 순위표 위에 따로 보여준다.
   (싫어요가 분명히 쌓인 영역은 다시 권하지 않는다. 반응이 적어 판단이 약한 영역만 고른다.)
합계(1+2)는 -4 ~ +4로 자른다. 신선도·출처 등급(최대 6점 안팎)을 뒤집지 않으면서 순서를 바꿀 만한 크기다.

신호 → 라벨 (글마다 하나, y는 -1 ~ +1):
- 좋아요/싫어요를 눌렀으면 그것이 전부다: +1 / -1 (같은 글에 여러 번 눌렀으면 마지막 것, 취소했으면 없음).
- 누르지 않았으면 읽은 기록으로 약하게: 펼침 +0.15, 읽은 시간 20초 +0.15·60초 +0.15 더, 원문 클릭 +0.25,
  긴 글을 70% 넘게 내려 읽음 +0.15 (최대 +0.6). 펼치지도 클릭하지도 않고 제목만 보고 지나친 날마다 -0.1 (최대 -0.3).
- 오래된 신호일수록 덜 믿는다: 무게 = 0.5 ^ (지난 날수 / 60).
"""
from __future__ import annotations

import datetime as dt
import json
import re
from dataclasses import dataclass, field
from pathlib import Path

import taste

ROOT = Path(__file__).resolve().parent.parent
INTERESTS = ROOT / "collector" / "interests.json"
CONTENT = ROOT / "web" / "src" / "content"
INBOX = ROOT / "data" / "inbox"
SIGNALS = ROOT.parent / "ai-brief-transcripts" / "signals"  # 사이트 쪽 경로는 web/src/lib/signals.ts의 SIGNAL_REPO·SIGNAL_DIR

MORE_PTS, LESS_PTS = 2, -3
CONTENT_PTS = 4          # 내용 유사도 -1~+1을 점수로 옮기는 배율
CLAMP = 4
HALF_LIFE_DAYS = 60
EXPLORE_MIN_LABELS = 8   # 라벨이 이만큼 쌓이기 전에는 모든 후보가 '모르는 영역'이라 탐색 몫이 뜻이 없다
EXPLORE_POOL = 40        # 화제성(관심 점수 뺀 점수) 상위 몇 개 안에서 고르나
EXPLORE_N = 3
EXPLORE_SUPPORT = 0.1    # 닮은 라벨의 무게 합이 이보다 작으면 '아직 잘 모르는 영역'


@dataclass
class Pref:
    points: int
    why: list[str] = field(default_factory=list)
    unexplored: bool = False  # 닮은 라벨이 거의 없음
    content: float = 0.0


# ---------- 직접 지정 ----------

def load_interests() -> dict:
    data = json.loads(INTERESTS.read_text(encoding="utf-8")) if INTERESTS.exists() else {}
    empty = {"categories": [], "sources": [], "keywords": []}
    return {side: {**empty, **data.get(side, {})} for side in ("more", "less")}


def site_key(url: str) -> str:
    """출처를 묶는 단위: 도메인. X는 계정까지 (x.com/openai)."""
    from urllib.parse import urlparse

    p = urlparse(url)
    host = p.netloc.lower().removeprefix("www.").replace("twitter.com", "x.com")
    if host == "x.com":
        handle = p.path.strip("/").split("/")[0].lower()
        return f"x.com/{handle}" if handle else host
    return host


def designated(group: list[dict], interests: dict) -> tuple[int, list[str]]:
    cats = {r.get("category_hint") for r in group}
    sites = {site_key(r["url"]) for r in group}
    srcs = {r["source"] for r in group}
    text = " ".join(r["title"] + " " + r.get("summary", "")[:300] for r in group).lower()
    pts, why = 0, []
    for side, unit in (("more", MORE_PTS), ("less", LESS_PTS)):
        rule = interests[side]
        hits = [c for c in rule["categories"] if c in cats]
        hits += [s for s in rule["sources"] if s in srcs or s in sites]
        hits += [k for k in rule["keywords"] if k.lower() in text]
        if hits:
            pts += unit * len(hits)
            why.append(("관심 지정 " if side == "more" else "비관심 지정 ") + "·".join(hits))
    return pts, why


# ---------- 신호 → 라벨 ----------

def load_events(root: Path | None = None) -> list[dict]:
    root = root or SIGNALS
    events = []
    for f in sorted(root.rglob("*.json")) if root.exists() else []:
        try:
            events += [e for e in json.loads(f.read_text(encoding="utf-8")) if isinstance(e, dict) and e.get("id")]
        except (OSError, ValueError):
            continue  # 깨진 파일 하나 때문에 순위표를 멈추지 않는다
    return events


def _parse(at: str) -> dt.datetime:
    return dt.datetime.fromisoformat(at.replace("Z", "+00:00"))


def label_values(events: list[dict], now: dt.datetime) -> dict[str, tuple[float, float, str]]:
    """글 id → (y, 무게, 설명)."""
    by_id: dict[str, list[dict]] = {}
    for e in sorted(events, key=lambda e: e.get("at", "")):
        by_id.setdefault(e["id"], []).append(e)
    out = {}
    for pid, evs in by_id.items():
        last = _parse(evs[-1]["at"])
        weight = 0.5 ** (max(0.0, (now - last).total_seconds() / 86400) / HALF_LIFE_DAYS)
        votes = [e for e in evs if e["t"] == "vote"]
        if votes and votes[-1].get("v"):
            v = votes[-1]
            out[pid] = (float(v["v"]), weight, "·".join(["좋아요" if v["v"] > 0 else "싫어요", *v.get("why", [])]))
            continue
        opened = any(e["t"] == "open" for e in evs)
        clicked = any(e["t"] == "click" for e in evs)
        sec = sum(e.get("sec", 0) for e in evs if e["t"] == "dwell")
        depth = max([e.get("depth", 0) for e in evs if e["t"] == "dwell"] or [0])
        if opened or clicked or sec:
            y = 0.15 * opened + 0.15 * (sec >= 20) + 0.15 * (sec >= 60) + 0.25 * clicked + 0.15 * (depth >= 0.7)
            out[pid] = (min(0.6, y), weight, f"읽음 {sec}초" + (" ·원문 클릭" if clicked else ""))
        else:
            days = len({e["at"][:10] for e in evs if e["t"] == "seen"})
            if days:
                out[pid] = (-0.1 * min(3, days), weight, f"보고 지나침 {days}일")
    return out


def candidate_text(r: dict) -> str:
    """수집 후보를 비교용 텍스트로. 라벨 글의 원문판과 새 후보가 같은 모양이어야 한다."""
    return r["title"] + ". " + r.get("summary", "")[:300]


def inbox_texts() -> dict[str, str]:
    """수집 후보 url → 비교용 텍스트. 라벨 글의 원문판을 찾는 데 쓴다."""
    out = {}
    for f in sorted(INBOX.glob("*.jsonl")):
        for line in f.read_text(encoding="utf-8").splitlines():
            try:
                r = json.loads(line)
            except ValueError:
                continue
            out[r["url"].rstrip("/")] = candidate_text(r)
    return out


def post_texts(pid: str, originals: dict[str, str]) -> list[str] | None:
    """cards/<id>, posts/<id> 글의 [제목·요약·본문 앞부분, 출처 후보 원문...]."""
    path = CONTENT / f"{pid}.md"
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8")
    parts = text.split("---", 2)
    fm, body = (parts[1], parts[2]) if len(parts) == 3 else ("", text)
    title = (re.search(r"^title: (.*)", fm, re.M) or [None, ""])[1].strip()
    if title.startswith('"'):
        try:
            title = json.loads(title)  # 따옴표 안의 \" 풀기
        except ValueError:
            title = title.strip('"')
    block = re.search(r"^summary:\n((?:\s+- .*\n?)+)", fm, re.M)  # 긴 글의 3줄 요약
    summary = " ".join(s.strip().strip('"') for s in re.findall(r"^\s+- (.*)", block.group(1), re.M)) if block else ""
    urls = [u.strip('"').rstrip("/") for u in re.findall(r"^\s+url: (\S+)", fm, re.M)]
    return [f"{title}\n{summary}\n{body.strip()[:600]}"] + [originals[u] for u in urls if u in originals]


def short(title: str, n: int = 24) -> str:
    return title if len(title) <= n else title[: n - 1] + "…"


# ---------- 순위표에 붙이기 ----------

class Preferences:
    def __init__(self, now: dt.datetime, embedder: taste.Embedder | None = None):
        self.interests = load_interests()
        values = label_values(load_events(), now)
        originals = inbox_texts() if values else {}
        labels = []
        for pid, (y, w, note) in values.items():
            texts = post_texts(pid, originals)
            if texts:
                title = texts[0].split("\n", 1)[0]
                labels.append(taste.Label(pid, texts, y, w, f"'{short(title)}' {note}"))
        self.n_labels = len(labels)
        self.taste = taste.Taste(labels, embedder)

    def status(self) -> str:
        if not self.n_labels:
            return "취향 라벨 0개 — 반응·읽은 기록이 쌓이면 내용 유사도 점수가 붙는다"
        if not self.taste.ready:
            return f"취향 라벨 {self.n_labels}개, 내용 유사도 꺼짐 ({self.taste.embedder.error})"
        return f"취향 라벨 {self.n_labels}개로 내용 유사도 점수를 붙임"

    def score_groups(self, groups: list[list[dict]]) -> list[Pref]:
        """같은 사건 묶음마다 관심 점수. 내용은 묶음의 대표 후보(첫 번째)로 본다."""
        texts = [candidate_text(g[0]) for g in groups]
        matches = self.taste.match_many(texts)
        out = []
        for g, m in zip(groups, matches):
            pts, why = designated(g, self.interests)
            cpts = round(m.value * CONTENT_PTS)
            if cpts:
                pts += cpts
                why.append(f"취향 {cpts:+d} (닮은 글: " + " / ".join(l.note for l, _ in m.neighbors[:2]) + ")")
            out.append(Pref(max(-CLAMP, min(CLAMP, pts)), why, m.support < EXPLORE_SUPPORT, m.value))
        return out

    def explore(self, base_scores: list[float], prefs: list[Pref], skip: list[bool]) -> list[int]:
        """탐색 후보: 관심 점수를 뺀 점수 상위 EXPLORE_POOL 안에서, 아직 잘 모르는 영역인 것."""
        if not self.taste.ready or self.n_labels < EXPLORE_MIN_LABELS:
            return []
        order = sorted(range(len(base_scores)), key=lambda i: -base_scores[i])[:EXPLORE_POOL]
        picks = [i for i in order if not skip[i] and prefs[i].unexplored]
        return picks[:EXPLORE_N]
