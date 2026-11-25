"""(Mac에서 실행) 글쓰기 후보 영상의 자막을 받아 비공개 저장소에 넣는다.

클라우드 서버에서는 유튜브가 자막 요청을 막아서, 사용자 Mac이 대신 받아 둔다.
글쓰기 작업은 비공개 저장소(clock-droid/ai-brief-transcripts)를 함께 받아 자막을 읽는다.

사용: python mac_transcripts.py <ai-brief 저장소 경로> <자막 저장소 경로>
대상: inbox의 영상 후보 중 공개 4일 이내, 아직 안 쓰고 안 건너뛴 것, 그리고 수집 대상인 것
      (핵심 인물·조회 2만 이상·1차 원천 채널 — transcript_queue.is_target).
속도: 유튜브가 몰린 요청을 몇 시간씩 막으므로(429) 한 회차에 MAX_PER_RUN개만, 요청 사이 PAUSE초를 둔다.
      막히면 그 회차는 바로 멈추고, 실패한 영상은 1→3→6시간 뒤 다시 시도한다 (transcript_queue).
자막은 확인용이다. 사이트에는 요약과 1~2문장 인용만 싣는다 (WRITING.md 7절).
"""
from __future__ import annotations

import datetime as dt
import glob
import json
import sys
import time
from pathlib import Path

MAX_PER_RUN = 4
PAUSE = 30  # 초
KEEP_DAYS = 7


def main() -> int:
    repo, out = Path(sys.argv[1]), Path(sys.argv[2])
    sys.path.insert(0, str(repo / "collector"))
    import rank
    import transcript_queue as q
    rank.DATA, rank.CONTENT = repo / "data", repo / "web" / "src" / "content"

    from youtube_transcript_api import YouTubeTranscriptApi

    now = dt.datetime.now(dt.timezone.utc)
    tiers = {s["id"]: s.get("tier", 2) for s in json.loads((repo / "collector" / "sources.json").read_text())["sources"]}
    done = rank.written_urls() | rank.skipped_urls()
    index = q.load_index(out)

    cands, seen = [], set()
    for f in glob.glob(str(repo / "data" / "inbox" / "*.jsonl")):
        for line in open(f, encoding="utf-8"):
            r = json.loads(line)
            vid = q.video_id(r["url"]) if r.get("video") else None
            if not vid or vid in seen or r["url"].rstrip("/") in done or not r.get("published"):
                continue
            seen.add(vid)
            if q.status(r, index, out, now, tiers, rank.KEY_PEOPLE) == "wait" and q.due(r, index, now):
                cands.append((r.get("views") or 0, vid, r))
    cands.sort(key=lambda x: -x[0])

    api = YouTubeTranscriptApi()
    got, tried, blocked = 0, 0, None
    for _, vid, r in cands[:MAX_PER_RUN]:
        if tried:
            time.sleep(PAUSE)
        tried += 1
        try:
            parts = api.fetch(vid, languages=["en", "ko", "en-US", "en-GB"])
        except Exception as exc:
            error = type(exc).__name__
            index[vid] = q.failure_entry(index.get(vid), r, error, now)
            if error in q.BLOCK_ERRORS:
                blocked = error
                break
            continue
        lines = [f"[{int(p.start // 60):02d}:{int(p.start % 60):02d}] {p.text}" for p in parts]
        (out / f"{vid}.txt").write_text("\n".join(lines), encoding="utf-8")
        index[vid] = {"url": r["url"], "title": r["title"], "fetched": now.isoformat(), "lines": len(lines)}
        got += 1

    # 오래된 자막 정리
    for vid, meta in list(index.items()):
        if now - dt.datetime.fromisoformat(meta["fetched"]) > dt.timedelta(days=KEEP_DAYS):
            (out / f"{vid}.txt").unlink(missing_ok=True)
            del index[vid]
    (out / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=1, sort_keys=True))
    note = f" · 유튜브 차단({blocked})으로 이 회차 중단" if blocked else ""
    print(f"받을 차례 {len(cands)}개 중 {tried}개 시도, 자막 {got}개 받음{note}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
