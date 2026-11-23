"""(Mac에서 실행) 글쓰기 후보 영상의 자막을 받아 비공개 저장소에 넣는다.

클라우드 서버에서는 유튜브가 자막 요청을 막아서, 사용자 Mac이 대신 받아 둔다.
글쓰기 작업은 비공개 저장소(clock-droid/ai-brief-transcripts)를 함께 받아 자막을 읽는다.

사용: python mac_transcripts.py <ai-brief 저장소 경로> <자막 저장소 경로>
대상: inbox의 영상 후보 중 공개 4일 이내, 아직 안 쓴 것, 그리고
      핵심 인물이 나오거나 / 조회 2만 이상이거나 / 1차 원천 채널(tier 1)인 것. 한 번에 최대 15개.
자막은 확인용이다. 사이트에는 요약과 1~2문장 인용만 싣는다 (WRITING.md 7절).
"""
from __future__ import annotations

import datetime as dt
import glob
import json
import re
import sys
from pathlib import Path

MAX_PER_RUN = 15
KEEP_DAYS = 7
WINDOW = dt.timedelta(days=4)


def main() -> int:
    repo, out = Path(sys.argv[1]), Path(sys.argv[2])
    sys.path.insert(0, str(repo / "collector"))
    from rank import KEY_PEOPLE, skipped_urls, written_urls  # 같은 판단 기준을 쓴다
    import rank
    rank.DATA, rank.CONTENT = repo / "data", repo / "web" / "src" / "content"

    from youtube_transcript_api import YouTubeTranscriptApi

    now = dt.datetime.now(dt.timezone.utc)
    tiers = {s["id"]: s.get("tier", 2) for s in json.loads((repo / "collector" / "sources.json").read_text())["sources"]}
    done = written_urls() | skipped_urls()
    index_path = out / "index.json"
    index = json.loads(index_path.read_text()) if index_path.exists() else {}

    cands = []
    for f in glob.glob(str(repo / "data" / "inbox" / "*.jsonl")):
        for line in open(f, encoding="utf-8"):
            r = json.loads(line)
            if not r.get("video") or r["url"].rstrip("/") in done:
                continue
            vid = re.search(r"v=([\w-]{11})", r["url"])
            if not vid or vid.group(1) in index or not r.get("published"):
                continue
            if now - dt.datetime.fromisoformat(r["published"]) > WINDOW:
                continue
            text = r["title"] + " " + r.get("summary", "")[:300]
            important = KEY_PEOPLE.search(text) or (r.get("views") or 0) >= 20_000 or tiers.get(r["source"]) == 1
            if important:
                cands.append((r.get("views") or 0, vid.group(1), r))
    cands.sort(key=lambda x: -x[0])

    api = YouTubeTranscriptApi()
    got = 0
    for _, vid, r in cands[:MAX_PER_RUN]:
        try:
            parts = api.fetch(vid, languages=["en", "ko", "en-US", "en-GB"])
        except Exception as exc:
            index[vid] = {"url": r["url"], "title": r["title"], "fetched": now.isoformat(), "error": type(exc).__name__}
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
    index_path.write_text(json.dumps(index, ensure_ascii=False, indent=1, sort_keys=True))
    print(f"후보 {len(cands)}개 중 자막 {got}개 받음")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
