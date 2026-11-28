"""유료 기사 본문 대기열: Mac 본문 수집(mac_paywall.py)과 순위표(rank.py)가 함께 쓰는 판단 기준.

사용자가 구독(경희대 학생 혜택 WSJ)으로 Aside 브라우저에 로그인해 두면,
Mac이 순위표에 오를 만한 유료 기사 몇 건의 본문을 받아 비공개 저장소의 paywall/ 폴더에 둔다.
글쓰기 작업은 그 본문을 원문으로 읽는다. 사이트에는 요약과 1~2문장 인용만 싣는다 (WRITING.md 7절).

본문 상태 (paywall/index.json 기준, 키는 기사 URL):
- have      본문 파일이 있음
- wait      아직 받는 중 (Mac이 다음 회차에 받는다)
- gave_up   받지 못함 (로그인 풀림·형식 변경 등으로 재시도 횟수 초과, 또는 발표 48시간 경과)
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
from pathlib import Path
from urllib.parse import urlsplit

# 구독으로 본문을 읽을 수 있는 사이트 (도메인 → 표시 이름)
SITES = {"wsj.com": "WSJ"}
WINDOW = dt.timedelta(hours=48)  # rank.WINDOW_H와 같다
MAX_ATTEMPTS = 3
DIR = "paywall"


def site(url: str) -> str | None:
    host = urlsplit(url).hostname or ""
    return next((name for domain, name in SITES.items() if host == domain or host.endswith("." + domain)), None)


def key(url: str) -> str:
    """추적용 쿼리(?mod=rss_...)를 뗀 URL."""
    return url.split("?")[0].split("#")[0].rstrip("/")


def filename(url: str) -> str:
    return hashlib.sha1(key(url).encode("utf-8")).hexdigest()[:16] + ".txt"


def load_index(handoff: Path) -> dict:
    path = handoff / DIR / "index.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def status(record: dict, index: dict, handoff: Path, now: dt.datetime) -> str:
    if (handoff / DIR / filename(record["url"])).exists():
        return "have"
    entry = index.get(key(record["url"]))
    published = record.get("published")
    if published and now - dt.datetime.fromisoformat(published) > WINDOW:
        return "gave_up"
    if entry and entry.get("attempts", 0) >= MAX_ATTEMPTS:
        return "gave_up"
    return "wait"
