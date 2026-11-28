"""사용자 관심도: 순위표(rank.py) 점수에 더하는 가산·감산과 탐색 몫. 핵심 계산은 taste.py, 이 파일은 이 프로젝트와의 연결.

세 가지를 쓴다.
1. 직접 지정 (collector/interests.json): "더 보고 싶은 것 / 덜 보고 싶은 것"으로 적은 분야·출처·낱말. 항목마다 +2 / -3.
2. 내용 유사도 (taste.py): 사이트 주인의 반응과 읽은 기록이 붙은 글을 라벨로 삼아, 새 후보가 좋아한 글과 닮았으면 +,
   싫어한 글과 닮았으면 -. -4 ~ +4.
   신호는 사이트(web/src/lib/signals.ts)가 비공개 저장소 ai-brief-taste의 signals/ 아래 JSON 파일로 올린다.
   글쓰기 작업이 이 저장소를 옆 폴더에 받아 두므로 여기서는 파일만 읽는다. 공개 저장소(data/)로 옮기지 않는다.
3. 출처·분류 반응률: 사이트에 실린 카드가 보였을 때 열어 봤는지를 출처(도메인·X 계정)와 분류별로 세어,
   전체 평균보다 잘 열리는 쪽은 +, 늘 지나치는 쪽은 -. 노출이 적으면 평균 쪽으로 당겨(AFF_PRIOR) 몇 번의 우연에 흔들리지 않는다.
   오래된 반응일수록 덜 믿으므로, 한동안 덜 실린 출처도 시간이 지나면 0으로 돌아온다.
4. 자동 조정 (tune.py): 2와 3을 얼마나 쓸지는 고정하지 않는다. 매 실행 지난 날들(최대 2주)을 하루씩 되짚어 보며
   "그 전 신호로 매긴 점수"가 "그 뒤 실제 반응"과 얼마나 맞았는지 재고, 더 잘 맞는 설정이 분명할 때만 바꾼다.
   조정 결과는 순위표 머리 한 줄(공개 저장소에 올라가지 않는 data/shortlist.md)에만 남는다.
5. 탐색 몫: 취향에 갇히지 않도록, 화제성은 높은데 아직 반응이 거의 없는 영역의 후보를 순위표 위에 따로 보여준다.
   (싫어요가 분명히 쌓인 영역은 다시 권하지 않는다. 반응이 적어 판단이 약한 영역만 고른다.)
합계(1+2+3)는 -4 ~ +4로 자른다. 신선도·출처 등급(최대 6점 안팎)을 뒤집지 않으면서 순서를 바꿀 만한 크기다.

신호 → 라벨 (글마다 하나, y는 -1 ~ +1):
- 좋아요/싫어요를 눌렀으면 그것이 전부다: +1 / -1 (같은 글에 여러 번 눌렀으면 마지막 것, 취소했으면 없음).
  싫어요 이유가 글 품질 쪽(너무 뻔함·과장)뿐이면 주제 자체가 싫은 건 아니므로 -0.5.
- 누르지 않았으면 읽은 기록으로 아주 약하게 (최대 +0.15, 좋아요의 7분의 1 남짓):
  펼침 +0.03, 읽은 시간 20초 +0.03·60초 +0.03 더, 긴 글을 70% 넘게 내려 읽음 +0.03, 원문 클릭 +0.1.
  별로인 글도 오래 펼쳐 둘 때가 있어 펼침·읽은 시간은 거의 믿지 않는다 (2026-11-25 사용자 판단). 원문 클릭은 의도가 더 분명해 조금 더 쳐 준다. 펼치지도 클릭하지도 않고 제목만 보고 지나친 날마다 -0.1 (최대 -0.3).
- 오래된 신호일수록 덜 믿는다: 무게 = 0.5 ^ (지난 날수 / 60).
"""
from __future__ import annotations

import datetime as dt
import json
import math
import re
from dataclasses import dataclass, field
from pathlib import Path

import taste
import tune

ROOT = Path(__file__).resolve().parent.parent
INTERESTS = ROOT / "collector" / "interests.json"
CONTENT = ROOT / "web" / "src" / "content"
INBOX = ROOT / "data" / "inbox"
SIGNALS = ROOT.parent / "ai-brief-taste" / "signals"  # 사이트 쪽 경로는 web/src/lib/signals.ts의 SIGNAL_REPO·SIGNAL_DIR

MORE_PTS, LESS_PTS = 2, -3
CONTENT_PTS = 4          # 내용 유사도 -1~+1을 점수로 옮기는 배율
CLAMP = 4
HALF_LIFE_DAYS = 60
EXPLORE_MIN_LABELS = 8   # 좋아요·싫어요를 누른 글이 이만큼 쌓이기 전에는 모든 후보가 '모르는 영역'이라 탐색 몫이 뜻이 없다
EXPLORE_POOL = 40        # 화제성(관심 점수 뺀 점수) 상위 몇 개 안에서 고르나
EXPLORE_N = 3
EXPLORE_SUPPORT = 0.1    # 닮은 라벨의 무게 합이 이보다 작으면 '아직 잘 모르는 영역'
READ_MAX = 0.15         # 버튼 없이 읽기만 한 글의 최대 y
AFF_PRIOR = 8            # 출처·분류 반응률을 전체 평균 쪽으로 당기는 가상 노출 수 (대부분의 출처는 노출이 몇 번뿐이라 크게 당긴다)
TUNE_MAX_DAYS = 14       # 자동 조정이 되짚어 보는 최대 날수 (신호가 있는 날만)
TUNE_MIN_ITEMS = 15      # 구간에 처음 보인 카드가 이보다 적으면 그 구간은 평가하지 않는다
QUALITY_REASONS = {"너무 뻔함", "과장"}  # 주제가 아니라 그 글이 별로라는 이유 (web/src/lib/signals.ts의 DISLIKE_REASONS 중)


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


def decay(last: dt.datetime, now: dt.datetime) -> float:
    """오래된 신호일수록 덜 믿는다: 0.5 ^ (지난 날수 / HALF_LIFE_DAYS)."""
    return 0.5 ** (max(0.0, (now - last).total_seconds() / 86400) / HALF_LIFE_DAYS)


def label_values(events: list[dict], now: dt.datetime) -> dict[str, tuple[float, float, str]]:
    """글 id → (y, 무게, 설명)."""
    out = {}
    for pid, evs in group_events(events).items():
        last = _parse(evs[-1]["at"])
        weight = decay(last, now)
        votes = [e for e in evs if e["t"] == "vote"]
        if votes and votes[-1].get("v"):
            v, why = votes[-1], votes[-1].get("why", [])
            y = float(v["v"])
            if y < 0 and why and set(why) <= QUALITY_REASONS:
                y = -0.5
            out[pid] = (y, weight, "·".join(["좋아요" if y > 0 else "싫어요", *why]))
            continue
        opened = any(e["t"] == "open" for e in evs)
        clicked = any(e["t"] == "click" for e in evs)
        sec = sum(e.get("sec", 0) for e in evs if e["t"] == "dwell")
        depth = max([e.get("depth", 0) for e in evs if e["t"] == "dwell"] or [0])
        if opened or clicked or sec:
            y = 0.03 * (opened + (sec >= 20) + (sec >= 60) + (depth >= 0.7)) + 0.1 * clicked
            out[pid] = (min(READ_MAX, y), weight, f"읽음 {sec}초" + (" ·원문 클릭" if clicked else ""))
        else:
            days = len({e["at"][:10] for e in evs if e["t"] == "seen"})
            if days:
                out[pid] = (-0.1 * min(3, days), weight, f"보고 지나침 {days}일")
    return out


def grade(evs: list[dict]) -> float:
    """보인 글에 대한 실제 반응 등급 (자동 조정의 정답): 좋아요 2, 열어 봄·원문 클릭 1, 지나침 0, 싫어요 -1."""
    votes = [e for e in evs if e["t"] == "vote"]
    v = votes[-1].get("v") if votes else 0
    if v:
        return 2.0 if v > 0 else -1.0
    return 1.0 if any(e["t"] in ("open", "click") for e in evs) else 0.0


def group_events(events: list[dict]) -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = {}
    for e in sorted(events, key=lambda e: e.get("at", "")):
        out.setdefault(e["id"], []).append(e)
    return out


def source_keys(r: dict) -> tuple[str, str | None]:
    """반응률을 세는 단위: (출처, 분류). 순위표 후보와 실린 카드의 원 후보에 똑같이 쓴다."""
    return site_key(r["url"]), r.get("category_hint")


class Affinity:
    """카드가 보였을 때 열어 본 비율을 출처·분류별로. 값은 전체 평균 대비 log2 비율을 -1~+1로 자른 것.
    카드만 센다 (긴 글은 들어오는 길이 달라 열어 보는 비율의 기준이 다르다).
    source(pid)는 그 카드가 된 수집 후보 — 순위표가 새 후보를 보는 것과 같은 출처·분류로 센다."""

    def __init__(self, events: list[dict], now: dt.datetime, source):
        self.site: dict[str, list[float]] = {}
        self.cat: dict[str, list[float]] = {}
        n = k = 0.0
        for pid, evs in group_events(events).items():
            r = source(pid) if pid.startswith("cards/") else None
            if not r:
                continue
            w = decay(_parse(evs[-1]["at"]), now)
            hit = w * (grade(evs) >= 1)
            n, k = n + w, k + hit
            site, cat = source_keys(r)
            for table, key in ((self.cat, cat), (self.site, site)):
                row = table.setdefault(key, [0.0, 0.0])
                row[0] += w
                row[1] += hit
        self.base = k / n if n else 0.0

    def _value(self, table: dict, key: str | None) -> float:
        if not self.base or key not in table:
            return 0.0
        n, k = table[key]
        rate = (k + AFF_PRIOR * self.base) / (n + AFF_PRIOR)
        return max(-1.0, min(1.0, math.log2(rate / self.base)))

    def of_site(self, key: str) -> float:
        return self._value(self.site, key)

    def of_cat(self, key: str | None) -> float:
        return self._value(self.cat, key)


def candidate_text(r: dict) -> str:
    """수집 후보를 비교용 텍스트로. 라벨 글의 원문판과 새 후보가 같은 모양이어야 한다."""
    return r["title"] + ". " + r.get("summary", "")[:300]


def inbox_records() -> dict[str, dict]:
    """수집 후보 url → 후보. 실린 글의 원 후보(원문판·출처·분류)를 찾는 데 쓴다."""
    out = {}
    for f in sorted(INBOX.glob("*.jsonl")):
        for line in f.read_text(encoding="utf-8").splitlines():
            try:
                r = json.loads(line)
            except ValueError:
                continue
            out[r["url"].rstrip("/")] = r
    return out


def _split(pid: str) -> tuple[str, str] | None:
    path = CONTENT / f"{pid}.md"
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8")
    parts = text.split("---", 2)
    return (parts[1], parts[2]) if len(parts) == 3 else ("", text)


def _urls(fm: str) -> list[str]:
    return [u.strip('"').rstrip("/") for u in re.findall(r"^\s+url: (\S+)", fm, re.M)]


def post_urls(pid: str) -> list[str]:
    """cards/<id>, posts/<id> 글의 출처 url들 (frontmatter 순서)."""
    split = _split(pid)
    return _urls(split[0]) if split else []


def post_texts(pid: str, originals: dict[str, str]) -> list[str] | None:
    """cards/<id>, posts/<id> 글의 [제목·요약·본문 앞부분, 출처 후보 원문...]."""
    split = _split(pid)
    if not split:
        return None
    fm, body = split
    title = (re.search(r"^title: (.*)", fm, re.M) or [None, ""])[1].strip()
    if title.startswith('"'):
        try:
            title = json.loads(title)  # 따옴표 안의 \" 풀기
        except ValueError:
            title = title.strip('"')
    block = re.search(r"^summary:\n((?:\s+- .*\n?)+)", fm, re.M)  # 긴 글의 3줄 요약
    summary = " ".join(s.strip().strip('"') for s in re.findall(r"^\s+- (.*)", block.group(1), re.M)) if block else ""
    urls = _urls(fm)
    return [f"{title}\n{summary}\n{body.strip()[:600]}"] + [originals[u] for u in urls if u in originals]


def short(title: str, n: int = 24) -> str:
    return title if len(title) <= n else title[: n - 1] + "…"


# ---------- 순위표에 붙이기 ----------

class Preferences:
    def __init__(self, now: dt.datetime, embedder: taste.Embedder | None = None, signals: Path | None = None):
        self.interests = load_interests()
        self.embedder = embedder or taste.Embedder()
        events = load_events(signals)
        self.records = inbox_records() if events else {}
        self.originals = {u: candidate_text(r) for u, r in self.records.items()}
        self._source: dict[str, dict | None] = {}
        self.choice = self._tune(events, now)
        self.config = self.choice.config
        labels = self._labels(events, now)
        self.n_labels = len(labels)
        self.n_strong = sum(abs(l.y) >= 0.5 for l in labels)  # 좋아요·싫어요를 누른 글만 센다
        self.taste = taste.Taste(labels, self.embedder)
        # 반응 글만 쓰는 설정이어도 '아직 모르는 영역'(탐색 몫)은 모든 라벨 기준으로 본다
        self.scoring_taste = taste.Taste(self._pick(labels, True), self.embedder) if self.config.strong_only else self.taste
        self.affinity = Affinity(events, now, self.source)

    def source(self, pid: str) -> dict | None:
        """실린 글이 된 수집 후보: 출처 url 중 수집함에 있는 첫 번째."""
        if pid not in self._source:
            self._source[pid] = next((self.records[u] for u in post_urls(pid) if u in self.records), None)
        return self._source[pid]

    def _labels(self, events: list[dict], now: dt.datetime) -> list[taste.Label]:
        labels = []
        for pid, (y, w, note) in label_values(events, now).items():
            texts = post_texts(pid, self.originals)
            if texts:
                title = texts[0].split("\n", 1)[0]
                labels.append(taste.Label(pid, texts, y, w, f"'{short(title)}' {note}"))
        return labels

    @staticmethod
    def _pick(labels: list[taste.Label], strong_only: bool) -> list[taste.Label]:
        return [l for l in labels if abs(l.y) >= 0.5] if strong_only else labels

    def _tune(self, events: list[dict], now: dt.datetime) -> tune.Choice:
        """하루(KST 자정 기준)씩 되짚기: 그 날 전 신호로 만든 점수 ↔ 그 날 처음 보인 카드의 실제 반응.
        구간 경계가 자정에 고정돼 있어 같은 날의 실행끼리는 같은 결론을 낸다. 오늘(아직 반응이 덜 쌓인 날)은 빼고,
        신호가 있는 가장 이른 날까지(최대 TUNE_MAX_DAYS일) 쓰므로 반응이 쌓일수록 근거가 늘어난다."""
        if not events:
            return tune.Choice(tune.DEFAULT, "자동 조정 보류 (신호 없음)")
        by_id = group_events(events)
        first = {pid: _parse(evs[0]["at"]) for pid, evs in by_id.items()}
        kst = dt.timezone(dt.timedelta(hours=9))
        today = now.astimezone(kst).replace(hour=0, minute=0, second=0, microsecond=0)
        earliest = min(first.values())
        windows = []
        for d in range(TUNE_MAX_DAYS, 0, -1):
            cut, end = today - dt.timedelta(days=d), today - dt.timedelta(days=d - 1)
            if end <= earliest:
                continue
            items = [(grade(evs), self.source(pid)) for pid, evs in by_id.items()
                     if pid.startswith("cards/") and cut <= first[pid] < end]
            items = [(g, r) for g, r in items if r]
            if len(items) < TUNE_MIN_ITEMS:
                continue
            past = [e for e in events if _parse(e["at"]) < cut]
            labels = self._labels(past, cut)
            texts = [candidate_text(r) for _, r in items]
            content = {s: [m.value for m in taste.Taste(self._pick(labels, s), self.embedder).match_many(texts)]
                       for s in (False, True)}
            aff = Affinity(past, cut, self.source)
            keys = [source_keys(r) for _, r in items]
            windows.append(tune.Window(cut.date().isoformat(), [g for g, _ in items], content,
                                       [aff.of_site(k[0]) for k in keys], [aff.of_cat(k[1]) for k in keys]))
        return tune.choose(windows)

    def status(self) -> str:
        if not self.n_labels:
            return "취향 라벨 0개 — 반응·읽은 기록이 쌓이면 내용 유사도 점수가 붙는다"
        if not self.taste.ready:
            return f"취향 라벨 {self.n_labels}개, 내용 유사도 꺼짐 ({self.embedder.error}). {self.choice.note}"
        return f"취향 라벨 {self.n_labels}개로 관심 점수를 붙임. {self.choice.note}"

    def score_groups(self, groups: list[list[dict]]) -> list[Pref]:
        """같은 사건 묶음마다 관심 점수. 내용·출처·분류는 묶음의 대표 후보(첫 번째)로 본다."""
        texts = [candidate_text(g[0]) for g in groups]
        matches = self.scoring_taste.match_many(texts)
        supports = self.taste.match_many(texts) if self.scoring_taste is not self.taste else matches
        out = []
        for g, m, sup in zip(groups, matches, supports):
            pts, why = designated(g, self.interests)
            site, cat = source_keys(g[0])
            cpts, spts, kpts = self.config.points(m.value, self.affinity.of_site(site), self.affinity.of_cat(cat))
            if cpts:
                why.append(f"취향 {cpts:+d} (닮은 글: " + " / ".join(l.note for l, _ in m.neighbors[:2]) + ")")
            if spts:
                why.append(f"출처 반응 {spts:+d}")
            if kpts:
                why.append(f"분류 반응 {kpts:+d}")
            pts += cpts + spts + kpts
            out.append(Pref(max(-CLAMP, min(CLAMP, pts)), why, sup.support < EXPLORE_SUPPORT, m.value))
        return out

    def explore(self, base_scores: list[float], prefs: list[Pref], skip: list[bool]) -> list[int]:
        """탐색 후보: 관심 점수를 뺀 점수 상위 EXPLORE_POOL 안에서, 아직 잘 모르는 영역인 것."""
        if not self.taste.ready or self.n_strong < EXPLORE_MIN_LABELS:
            return []
        order = sorted(range(len(base_scores)), key=lambda i: -base_scores[i])[:EXPLORE_POOL]
        picks = [i for i in order if not skip[i] and prefs[i].unexplored]
        return picks[:EXPLORE_N]
