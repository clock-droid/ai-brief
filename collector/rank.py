"""후보 순위표.

data/inbox의 후보 중 발표 48시간 이내이고 아직 글로 쓰지 않은 것을 같은 사건끼리 묶고,
중요도 점수를 매겨 상위 N개를 짧은 표로 낸다. 글쓰기 작업은 이 표를 위에서부터 검토한다 (WRITING.md 1절).

점수 구성 (높을수록 먼저 검토):
- 신선도: 6시간 이내 3, 12시간 2, 24시간 1, 48시간 0
- 출처 등급(sources.json tier): 1차 원천 3, 전문 매체 2, 국내 2차·대량 집계 0. X 원문은 2
- Techmeme이 트윗 자체를 기사로 올렸으면(발표 트윗) +2
- 특갤 화제: X 링크가 특갤 글에 올라왔으면 2, 그 글의 추천 10/20/40 이상이면 +1/+2/+3, 조회 3000 이상 +1
- HF 논문 추천 수: 20 이상 +1, 50 이상 +2
- 같은 사건을 다룬 출처 수: 출처 하나 늘 때마다 +1 (최대 +3)
- 이미 다룬 사건(묶음 안에 이미 실린 URL이 있음): -3
- 범위가 넓은 매체(sources.json broad)의 글이 AI·기술과 무관하면: -4
- 혁신성: 새 모델·논문·벤치마크·증명·발견·로봇 시연·오픈소스 공개 +2 / 인수·투자 유치·주가·소송·인사·정치 공방 -1
- 급상승 지표: GitHub 오늘 별 500/1000 이상 +1/+2, 허깅페이스 급상승 점수 100/300 이상 +1/+2

사용: python3 collector/rank.py [--top 60]
이미 검토하고 건너뛴 후보(data/skipped.jsonl)는 빠진다.
"""
from __future__ import annotations

import argparse
import datetime as dt
import glob
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
CONTENT = ROOT / "web" / "src" / "content"
OUT = DATA / "shortlist.md"
WINDOW_H = 48
VIDEO_WINDOW_H = 96  # 인터뷰·팟캐스트 영상

STOP = set("""the and for with from that this into over after about what will says said new how why are was has have its
their your more than just only also amid via per using use used can not but you all one two now our out who which when
https http com www status""".split())
AI_TECH = re.compile(
    r"\b(ai|a\.i\.|llm|gpt|claude|gemini|agent|robot|machine learning|neural|algorithm|chip|semiconductor|compute|data ?center|quantum|automation|software|brain-computer|bci)\b"
    r"|인공지능|에이전트|로봇|반도체|자동화|양자", re.I)
INNOVATION = re.compile(
    r"\b(launch(es|ed)?|release[sd]?|unveil\w*|introduc(es|ed|ing)|open[- ]?sourc\w*|open[- ]weights?|new model|"
    r"benchmark\w*|state[- ]of[- ]the[- ]art|sota|breakthrough|proof|proves?|proved|theorem|discover\w*|arxiv|"
    r"humanoid|outperform\w*|surpass\w*)\b"
    r"|공개|출시|증명|돌파|발견|벤치마크|신모델|오픈소스|시연|최초", re.I)
BUSINESS = re.compile(
    r"\b(acquir\w*|acquisition|raise[sd]?|raising|funding|valuation|ipo|stock|shares|lawsuit|sue[sd]?|suing|ceo|board|"
    r"investor\w*|merger|antitrust|probe|tariff\w*|lobby\w*|earnings|revenue|layoff\w*|scandal|resign\w*)\b"
    r"|인수|투자 유치|상장|주가|시총|소송|이사회|제소|실적|매출|정치", re.I)
TRENDING_SOURCES = {"github-trending", "hf-trending-models"}
PLACEHOLDER = re.compile(r"^(pic\.twitter\.com/\S+|https?://t\.co/\S+)$")


def now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def load_candidates() -> list[dict]:
    rows = []
    for f in sorted(glob.glob(str(DATA / "inbox" / "*.jsonl"))):
        for line in open(f, encoding="utf-8"):
            if line.strip():
                rows.append(json.loads(line))
    return rows


def written_urls() -> set[str]:
    urls = set()
    for p in glob.glob(str(CONTENT / "*" / "*.md")):
        urls |= {u.strip('"').rstrip("/") for u in re.findall(r"url: (\S+)", Path(p).read_text(encoding="utf-8"))}
    return urls


def skipped_urls() -> set[str]:
    """글쓰기 작업이 이미 검토하고 건너뛴 후보 (data/skipped.jsonl). 순위표에서 뺀다."""
    path = DATA / "skipped.jsonl"
    if not path.exists():
        return set()
    return {json.loads(l)["url"].rstrip("/") for l in path.read_text(encoding="utf-8").splitlines() if l.strip()}


def written_token_sets() -> list[set[str]]:
    """이미 실린 글마다 고유명사 위주 토큰 묶음. URL이 달라도 같은 사건이면 '이미 다룸'으로 잡기 위해 쓴다."""
    sets = []
    for p in glob.glob(str(CONTENT / "*" / "*.md")):
        text = re.sub(r"https?://\S+", " ", Path(p).read_text(encoding="utf-8"))
        sets.append({w.lower() for w in re.findall(r"[A-Za-z][A-Za-z0-9.\-]{2,}|[0-9]+[A-Za-z][A-Za-z0-9.\-]*", text)} - STOP)
    return sets


def covered(tk: set[str], written_sets: list[set[str]]) -> bool:
    latin = {t for t in tk if re.match(r"[a-z0-9]", t)}
    if len(latin) < 3:
        return False
    return any(len(latin & w) >= 3 and len(latin & w) / len(latin) >= 0.3 for w in written_sets)


def age_hours(r: dict) -> float:
    t = r.get("published") or r["collected"]
    return (now() - dt.datetime.fromisoformat(t)).total_seconds() / 3600


def display_title(r: dict) -> str:
    title = r["title"].strip()
    if (not title or PLACEHOLDER.match(title)) and r.get("signal"):
        return f"[특갤] {r['signal']['title']}"
    if ctx := r.get("context"):
        who = (r.get("tweet") or {}).get("author") or ""
        return f"{ctx['title']}  ← X {who}: {title[:60]}"
    return title


def tokens(r: dict) -> set[str]:
    tw = r.get("tweet") or {}
    # 트윗은 작성자 이름도 넣는다 — 같은 발언을 다룬 기사("Alexandr Wang says …")와 묶이도록
    text = " ".join([r["title"], (r.get("signal") or {}).get("title", ""), (r.get("context") or {}).get("title", ""),
                     tw.get("text", "")[:200], tw.get("author") or ""])
    text = re.sub(r"https?://\S+", " ", text)
    toks = set()
    for w in re.findall(r"[A-Za-z][A-Za-z0-9.\-]{2,}|[0-9]+[A-Za-z][A-Za-z0-9.\-]*|[가-힣]{3,}", text):
        w = w.lower().strip(".-")
        if w not in STOP and len(w) >= 3:
            toks.add(w)
    return toks


def item_score(r: dict, tiers: dict, broad: set, dc_signals: dict) -> tuple[int, list[str]]:
    why = []
    if r["source"] in broad and not AI_TECH.search(r["title"] + " " + r.get("summary", "")[:300]):
        return -4, ["AI·기술 무관"]
    a = age_hours(r)
    fresh = 3 if a <= 6 else 2 if a <= 12 else 1 if a <= 24 else 0
    score = fresh
    if r.get("tweet"):
        tier_pts = 2
    else:
        tier_pts = {1: 3, 2: 2, 3: 0}.get(tiers.get(r["source"], 2), 2)
    score += tier_pts
    if sig := r.get("signal"):
        live = dc_signals.get(sig["url"], {})
        rec, views = live.get("recommend", 0), live.get("views", 0)
        pts = 2 + (3 if rec >= 40 else 2 if rec >= 20 else 1 if rec >= 10 else 0) + (1 if views >= 3000 else 0)
        score += pts
        why.append(f"특갤 추천{rec}·조회{views}")
    # 제목(+Techmeme 기사 제목, 특갤 제목)만 본다. 요약까지 보면 잡음이 커진다.
    # 급상승 목록(GitHub·허깅페이스)은 자체 지표로 점수를 받으므로 혁신 가산을 주지 않는다.
    text = " ".join([r["title"], (r.get("context") or {}).get("title", ""), (r.get("signal") or {}).get("title", "")])
    innov, biz = bool(INNOVATION.search(text)), bool(BUSINESS.search(text))
    if innov and not biz and r["source"] not in TRENDING_SOURCES:
        score += 2
        why.append("혁신")
    elif biz and not innov:
        score -= 1
    if (st := r.get("stars_today")) is not None:
        score += 2 if st >= 1000 else 1 if st >= 500 else 0
        why.append(f"GitHub 오늘 별{st}")
    if (tr := r.get("trending")) is not None:
        score += 2 if tr >= 300 else 1 if tr >= 100 else 0
        why.append(f"HF 급상승{tr:.0f}")
    if r.get("video"):
        why.append("영상")
    if (vw := r.get("views")) is not None:
        score += 2 if vw >= 100_000 else 1 if vw >= 20_000 else 0
        why.append(f"조회{vw:,}")
    if (ctx := r.get("context")) and ctx.get("headline_tweet"):
        score += 2
        why.append("Techmeme 헤드라인 트윗")
    if (up := r.get("upvotes")) is not None:
        score += 2 if up >= 50 else 1 if up >= 20 else 0
        why.append(f"HF 추천{up}")
    return score, why


def cluster(rows: list[dict]) -> list[list[dict]]:
    groups: list[tuple[set[str], list[dict]]] = []
    for r in rows:
        tk = tokens(r)
        best = None
        for g in groups:
            shared = tk & g[0]
            if len(shared) >= 2 and len(shared) / max(1, min(len(tk), len(g[0]))) >= 0.34:
                best = g
                break
        if best:
            best[0].update(tk)
            best[1].append(r)
        else:
            groups.append((set(tk), [r]))
    return [g[1] for g in groups]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--top", type=int, default=60)
    args = ap.parse_args()

    srcs = json.loads((ROOT / "collector" / "sources.json").read_text())["sources"]
    tiers = {s["id"]: s.get("tier", 2) for s in srcs}
    broad = {s["id"] for s in srcs if s.get("broad")}
    dc_path = DATA / "dc_signals.json"
    dc_signals = json.loads(dc_path.read_text()) if dc_path.exists() else {}
    written = written_urls()
    written_sets = written_token_sets()

    fresh = [r for r in load_candidates() if age_hours(r) <= (VIDEO_WINDOW_H if r.get("video") else WINDOW_H)]
    # 같은 URL 중복 제거
    fresh = list({r["url"].rstrip("/"): r for r in fresh}.values())
    skipped = skipped_urls()
    fresh = [r for r in fresh if r["url"].rstrip("/") not in skipped]

    ranked = []
    for g in cluster(fresh):
        scored = [(item_score(r, tiers, broad, dc_signals), r) for r in g]
        scored.sort(key=lambda x: -x[0][0])
        (best_score, why), lead = scored[0]
        sources = {r["source"] for r in g}
        bonus = min(3, len(sources) - 1)
        done = any(r["url"].rstrip("/") in written for r in g) or covered(set().union(*(tokens(r) for r in g)), written_sets)
        total = best_score + bonus - (3 if done else 0)
        ranked.append({"score": total, "lead": lead, "members": [r for _, r in scored], "why": why,
                       "n_sources": len(sources), "done": done})
    # 이미 다룬 사건은 점수와 관계없이 뒤로 보낸다 (위쪽 자리를 새 소식에 쓰기 위해)
    ranked.sort(key=lambda x: (x["done"], -x["score"], age_hours(x["lead"])))

    lines = [f"# 후보 순위표 ({now().astimezone(dt.timezone(dt.timedelta(hours=9))).strftime('%m월 %d일 %H:%M')} KST)",
             "", f"발표 {WINDOW_H}시간 이내 후보 {len(fresh)}개 → 사건 {len(ranked)}개로 묶음. 상위 {args.top}개.",
             "점수 구성은 collector/rank.py 맨 위 설명 참고. 위에서부터 검토한다.", ""]
    for i, x in enumerate(ranked[: args.top], 1):
        lead = x["lead"]
        flags = []
        if x["n_sources"] > 1:
            flags.append(f"출처 {x['n_sources']}곳")
        if x["done"]:
            flags.append("이미 다룸 — 큰 진전 있을 때만")
        flags += x["why"]
        lines.append(f"{i}. **{x['score']}점** · {age_hours(lead):.0f}시간 전 · {lead['source_name']} — {display_title(lead)[:110]}")
        if flags:
            lines.append(f"   - {' · '.join(flags)}")
        for m in x["members"]:
            lines.append(f"   - {m['source']}: {m['url']}")
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
