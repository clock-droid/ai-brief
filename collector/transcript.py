"""유튜브 영상 자막을 받아 텍스트 파일로 남긴다 (글쓰기 작업이 영상 발언을 확인하는 용도).

사용: python3 collector/transcript.py <영상 URL 또는 id> [...]
결과: data/transcripts/<id>.txt (저장소에 커밋하지 않음)

공개 영상의 자동 자막을 youtube-transcript-api로 받는다. 설치돼 있지 않으면 설치 방법을 출력하고 끝낸다.
    pip install -q youtube-transcript-api
자막은 요약과 짧은 인용을 위한 확인 자료로만 쓴다. 자막 전문을 사이트에 싣지 않는다 (WRITING.md 7절).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "data" / "transcripts"
LANGS = ["en", "ko", "en-US", "en-GB"]


def video_id(s: str) -> str:
    m = re.search(r"(?:v=|youtu\.be/|/shorts/|/live/)([\w-]{11})", s)
    return m.group(1) if m else s.strip()


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
    except ImportError:
        print("youtube-transcript-api가 없음. 먼저: pip install -q youtube-transcript-api", file=sys.stderr)
        return 2
    OUT.mkdir(parents=True, exist_ok=True)
    api = YouTubeTranscriptApi()
    status = 0
    for arg in sys.argv[1:]:
        vid = video_id(arg)
        try:
            parts = api.fetch(vid, languages=LANGS)
        except Exception as exc:  # 자막 없음, 차단 등
            print(f"{vid}: 실패 ({type(exc).__name__}: {str(exc)[:150]})", file=sys.stderr)
            status = 3
            continue
        # 시각 표시를 남겨 인용 위치를 찾을 수 있게 한다: [mm:ss] 문장
        lines = [f"[{int(p.start // 60):02d}:{int(p.start % 60):02d}] {p.text}" for p in parts]
        path = OUT / f"{vid}.txt"
        path.write_text("\n".join(lines), encoding="utf-8")
        print(f"{vid}: {len(lines)}줄 → {path}")
    return status


if __name__ == "__main__":
    raise SystemExit(main())
