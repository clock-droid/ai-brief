"""(Mac에서 실행) 순위표에 오를 만한 유료 기사(WSJ)의 본문을 받아 비공개 저장소에 넣는다.

WSJ는 브라우저가 아닌 프로그램 요청을 로그인과 관계없이 막는다. 그래서 사용자가 구독 계정으로
로그인해 둔 Aside 브라우저로 기사를 열어 읽는다 (aside repl, collector/paywall.js).

사용: python mac_paywall.py <ai-brief 저장소 경로> <비공개 전달 저장소 경로>
대상: inbox 후보 중 paywall_queue.SITES 도메인의 기사로, 발표 48시간 이내, 아직 안 쓰고 안 건너뛰었고,
      AI·기술 관련인 것 (rank.item_score가 'AI·기술 무관' 감점을 주지 않은 것). 점수 높은 순.
속도: 구독 계정을 사람이 읽는 속도로만 쓴다. 한 회차에 MAX_PER_RUN건, 기사 사이 PAUSE초.
      로그인이 풀린 게 보이면 그 회차를 멈추고 실행 기록에 알린다 (Aside에서 다시 로그인해야 한다).
본문은 확인용이다. 사이트에는 요약과 1~2문장 인용만 싣는다 (WRITING.md 7절).
"""
from __future__ import annotations

import datetime as dt
import glob
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

MAX_PER_RUN = 3
PAUSE = 20  # 초
KEEP_DAYS = 7
HERE = Path(__file__).resolve().parent


class LoggedOut(Exception):
    pass


def read_article(url: str) -> dict:
    executable = shutil.which("aside") or str(Path.home() / ".local/bin/aside")
    script = "const input = " + json.dumps({"url": url}) + ";\n" + (HERE / "paywall.js").read_text()
    proc = subprocess.run([executable, "repl", script], capture_output=True, text=True, timeout=125)
    rows = [line[7:] for line in proc.stdout.splitlines() if line.startswith("RESULT ")]
    if proc.returncode or not rows:
        raise RuntimeError(f"Aside 응답 미완료 (exit={proc.returncode})")
    result = json.loads(rows[-1])
    if result["locked"]:
        raise LoggedOut
    if len(result["paragraphs"]) <= 3:
        raise RuntimeError("본문 문단을 찾지 못함 (페이지 형식 변경?)")
    return result


def main() -> int:
    repo, out = Path(sys.argv[1]), Path(sys.argv[2])
    sys.path.insert(0, str(repo / "collector"))
    import rank
    import paywall_queue as pq
    rank.DATA, rank.CONTENT = repo / "data", repo / "web" / "src" / "content"

    now = dt.datetime.now(dt.timezone.utc)
    srcs = json.loads((repo / "collector" / "sources.json").read_text())["sources"]
    tiers = {s["id"]: s.get("tier", 2) for s in srcs}
    broad = {s["id"] for s in srcs if s.get("broad")}
    # 사용자가 구독 로그인으로 받기를 허락한 건 AI 관련 기사뿐이다 (2026-11-28). 경제 섹션 출처(WSJ Markets 등)는 받지 않는다
    econ = {s["id"] for s in srcs if s.get("category") in rank.ECON_CATEGORIES}
    done = rank.written_urls() | rank.skipped_urls()
    folder = out / pq.DIR
    folder.mkdir(exist_ok=True)
    index = pq.load_index(out)

    cands, seen = [], set()
    for f in glob.glob(str(repo / "data" / "inbox" / "*.jsonl")):
        for line in open(f, encoding="utf-8"):
            r = json.loads(line)
            k = pq.key(r["url"])
            if not pq.site(r["url"]) or r["source"] in econ or k in seen or r["url"].rstrip("/") in done or not r.get("published"):
                continue
            seen.add(k)
            if pq.status(r, index, out, now) != "wait":
                continue
            score, why = rank.item_score(r, tiers, broad, {})
            if "AI·기술 무관" not in why:
                cands.append((score, r))
    cands.sort(key=lambda x: -x[0])

    got, tried, logged_out = 0, 0, False
    for _, r in cands[:MAX_PER_RUN]:
        if tried:
            time.sleep(PAUSE)
        tried += 1
        k = pq.key(r["url"])
        try:
            result = read_article(k)
        except LoggedOut:
            logged_out = True
            break
        except (RuntimeError, OSError, subprocess.SubprocessError, ValueError) as exc:
            prev = index.get(k, {})
            index[k] = {"title": r["title"], "fetched": now.isoformat(), "error": str(exc)[:200],
                        "attempts": prev.get("attempts", 0) + 1}
            continue
        body = "\n\n".join(result["paragraphs"])
        (folder / pq.filename(k)).write_text(f"{result['title']}\n{k}\n\n{body}\n", encoding="utf-8")
        index[k] = {"title": result["title"], "fetched": now.isoformat(), "chars": len(body)}
        got += 1

    # 오래된 본문 정리
    for k, meta in list(index.items()):
        if now - dt.datetime.fromisoformat(meta["fetched"]) > dt.timedelta(days=KEEP_DAYS):
            (folder / pq.filename(k)).unlink(missing_ok=True)
            del index[k]
    (folder / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=1, sort_keys=True))
    note = " · 로그인 풀림: Aside 브라우저에서 WSJ에 다시 로그인해야 함" if logged_out else ""
    print(f"유료 기사 받을 차례 {len(cands)}건 중 {tried}건 시도, 본문 {got}건 받음{note}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
