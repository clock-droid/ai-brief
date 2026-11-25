"""사용자 관심도: 순위표(rank.py) 점수에 더하는 가산·감산.

두 가지를 쓴다. 중요도를 글쓰기 작업이 정하지 않고 사용자 판단으로 조정하기 위해서다.
1. 직접 지정 (collector/interests.json): 사용자가 "더 보고 싶은 것 / 덜 보고 싶은 것"으로 적은 분야·출처·낱말.
   더 보고 싶음 +2, 덜 보고 싶음 -3 (항목마다, 합계는 아래 범위로 자름).
2. 반응 (data/feedback.json): 사이트 글 아래 "관심 있음 · 관심 없음"을 누르면 GitHub 이슈가 생기고,
   collect.py가 저장소 주인이 쓴 이슈만 받아 둔다. 반응한 글의 특징(분류·출처 주소·핵심 인물)마다 표를 모아
   같은 특징을 가진 후보에 특징당 ±1~2를 준다.
합계는 -4~+4로 자른다. 신선도·출처 등급(최대 6점 안팎)을 뒤집지 않으면서 순서를 바꿀 만한 크기다.
"""
from __future__ import annotations

import collections
import json
import re
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
INTERESTS = ROOT / "collector" / "interests.json"
FEEDBACK = ROOT / "data" / "feedback.json"
CONTENT = ROOT / "web" / "src" / "content"

MORE_PTS, LESS_PTS = 2, -3
CLAMP = 4


def load_interests() -> dict:
    data = json.loads(INTERESTS.read_text(encoding="utf-8")) if INTERESTS.exists() else {}
    empty = {"categories": [], "sources": [], "keywords": []}
    return {side: {**empty, **data.get(side, {})} for side in ("more", "less")}


def site_key(url: str) -> str:
    """출처를 묶는 단위: 도메인. X는 계정까지 (x.com/openai)."""
    p = urlparse(url)
    host = p.netloc.lower().removeprefix("www.").replace("twitter.com", "x.com")
    if host == "x.com":
        handle = p.path.strip("/").split("/")[0].lower()
        return f"x.com/{handle}" if handle else host
    return host


def people(text: str, key_people: re.Pattern) -> set[str]:
    return {f"인물:{m.group(0).lower()}" for m in key_people.finditer(text)}


def post_features(path: Path, key_people: re.Pattern) -> set[str]:
    """이미 실린 글의 특징. 반응을 후보 점수로 옮기는 다리."""
    text = path.read_text(encoding="utf-8")
    fm = text.split("---")[1] if text.startswith("---") else ""
    feats = set()
    if m := re.search(r"^category: (\w+)", fm, re.M):
        feats.add(f"분류:{m.group(1)}")
    feats |= {f"출처:{site_key(u.strip(chr(34)))}" for u in re.findall(r"^\s+url: (\S+)", fm, re.M)}
    title = (re.search(r"^title: (.*)", fm, re.M) or [None, ""])[1]
    feats |= people(title + " " + text[len(fm):][:400], key_people)
    return feats


def candidate_features(r: dict, key_people: re.Pattern) -> set[str]:
    feats = {f"출처:{site_key(r['url'])}"}
    if r.get("category_hint"):
        feats.add(f"분류:{r['category_hint']}")
    text = " ".join([r["title"], r.get("summary", "")[:300], (r.get("tweet") or {}).get("author") or ""])
    feats |= people(text, key_people)
    return feats


def learned_weights(key_people: re.Pattern) -> collections.Counter:
    """반응한 글마다 특징에 +1(관심 있음)/-1(관심 없음)을 더한다. 같은 글에 반응이 여럿이면 마지막 것만."""
    if not FEEDBACK.exists():
        return collections.Counter()
    latest = {}
    for fb in sorted(json.loads(FEEDBACK.read_text(encoding="utf-8")), key=lambda x: x["at"]):
        latest[fb["id"]] = fb["vote"]
    weights = collections.Counter()
    for post_id, vote in latest.items():
        path = CONTENT / f"{post_id}.md"
        if path.exists():
            for f in post_features(path, key_people):
                weights[f] += vote
    return weights


def score(group: list[dict], interests: dict, weights: collections.Counter, key_people: re.Pattern) -> tuple[int, list[str]]:
    """같은 사건 묶음의 관심 점수와 근거."""
    feats = set().union(*(candidate_features(r, key_people) for r in group))
    text = " ".join(r["title"] + " " + r.get("summary", "")[:300] for r in group).lower()
    srcs = {r["source"] for r in group}
    pts, why = 0, []
    for side, unit in (("more", MORE_PTS), ("less", LESS_PTS)):
        rule = interests[side]
        hits = [c for c in rule["categories"] if f"분류:{c}" in feats]
        hits += [s for s in rule["sources"] if s in srcs or f"출처:{s}" in feats]
        hits += [k for k in rule["keywords"] if k.lower() in text]
        if hits:
            pts += unit * len(hits)
            why.append(("관심 지정 " if side == "more" else "비관심 지정 ") + "·".join(hits))
    learned = {f: max(-2, min(2, weights[f])) for f in feats if weights.get(f)}
    if learned:
        pts += sum(learned.values())
        why.append("반응 " + " ".join(f"{f}{v:+d}" for f, v in sorted(learned.items(), key=lambda x: -abs(x[1]))[:3]))
    return max(-CLAMP, min(CLAMP, pts)), why
