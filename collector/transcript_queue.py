"""영상 자막 대기열: Mac 자막 수집(mac_transcripts.py)과 순위표(rank.py)가 함께 쓰는 판단 기준.

유튜브는 짧은 시간에 자막 요청이 몰리면 IP를 몇 시간 막는다(429, IpBlocked).
그래서 Mac은 한 번에 몇 개만 천천히 받고, 막히면 그 회차를 멈추고, 실패한 영상은 시간을 두고 다시 시도한다.

자막 상태 (자막 저장소의 index.json 기준):
- have      자막 파일이 있음
- wait      아직 받는 중 (처음 시도 전이거나, 재시도 예정)
- gave_up   끝내 못 받음 (자막 꺼짐·영상 없음 등 영구 실패, 재시도 횟수 초과, 공개 4일 경과)
- not_target Mac 수집 대상이 아님 (핵심 인물·조회 2만·1차 채널 어디에도 해당 안 됨)

글쓰기 작업은 wait인 영상을 건너뛰지 않고 다음 실행으로 넘기고,
gave_up·not_target인 영상은 영상 설명·같은 내용 보도로 확인한다 (WRITING.md 1절 5).
"""
from __future__ import annotations

import datetime as dt
import json
import re
from pathlib import Path

WINDOW = dt.timedelta(days=4)  # rank.VIDEO_WINDOW_H와 같다
RETRY_DELAYS = [dt.timedelta(hours=1), dt.timedelta(hours=3), dt.timedelta(hours=6)]
MAX_ATTEMPTS = len(RETRY_DELAYS) + 1
VIEWS_THRESHOLD = 20_000

# 다시 시도해도 결과가 같은 실패
PERMANENT_ERRORS = {"TranscriptsDisabled", "NoTranscriptFound", "VideoUnavailable", "VideoUnplayable",
                    "AgeRestricted", "InvalidVideoId", "NotTranslatable"}
# 유튜브가 요청을 막은 것. 이 회차는 더 요청하지 않는다
BLOCK_ERRORS = {"IpBlocked", "RequestBlocked", "YouTubeRequestFailed", "PoTokenRequired"}


def video_id(url: str) -> str | None:
    m = re.search(r"(?:v=|youtu\.be/|/shorts/|/live/)([\w-]{11})", url)
    return m.group(1) if m else None


def load_index(transcripts: Path) -> dict:
    path = transcripts / "index.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def is_target(record: dict, tiers: dict, key_people: re.Pattern) -> bool:
    """Mac이 자막을 받아 둘 영상인가: 핵심 인물이 나오거나, 조회 2만 이상이거나, 1차 원천 채널."""
    text = record["title"] + " " + record.get("summary", "")[:300]
    return bool(key_people.search(text)) or (record.get("views") or 0) >= VIEWS_THRESHOLD or tiers.get(record["source"]) == 1


def _attempts(entry: dict) -> int:
    # 재시도가 생기기 전 기록은 attempts가 없다: 한 번 실패한 것으로 본다
    return entry.get("attempts", 1)


def retry_after(entry: dict) -> dt.datetime:
    if "retry_after" in entry:
        return dt.datetime.fromisoformat(entry["retry_after"])
    return dt.datetime.fromisoformat(entry["fetched"]) + RETRY_DELAYS[0]


def failure_entry(prev: dict | None, record: dict, error: str, now: dt.datetime) -> dict:
    attempts = (_attempts(prev) if prev and prev.get("error") else 0) + 1
    entry = {"url": record["url"], "title": record["title"], "fetched": now.isoformat(), "error": error, "attempts": attempts}
    if error not in PERMANENT_ERRORS and attempts < MAX_ATTEMPTS:
        entry["retry_after"] = (now + RETRY_DELAYS[attempts - 1]).isoformat()
    return entry


def status(record: dict, index: dict, transcripts: Path, now: dt.datetime, tiers: dict, key_people: re.Pattern) -> str:
    vid = video_id(record["url"])
    if vid and (transcripts / f"{vid}.txt").exists():
        return "have"
    entry = index.get(vid or "")
    published = record.get("published")
    if published and now - dt.datetime.fromisoformat(published) > WINDOW:
        return "gave_up" if entry else "not_target"
    if entry and entry.get("error"):
        if entry["error"] in PERMANENT_ERRORS or _attempts(entry) >= MAX_ATTEMPTS:
            return "gave_up"
        return "wait"
    return "wait" if is_target(record, tiers, key_people) else "not_target"


def due(record: dict, index: dict, now: dt.datetime) -> bool:
    """지금 요청해도 되는가 (처음이거나 재시도 시각이 지남)."""
    entry = index.get(video_id(record["url"]) or "")
    if not entry:
        return True
    if not entry.get("error") or entry["error"] in PERMANENT_ERRORS or _attempts(entry) >= MAX_ATTEMPTS:
        return False
    return now >= retry_after(entry)
