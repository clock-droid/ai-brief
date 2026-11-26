"""Render direct sources independently of the main ranking and its top-N cutoff."""
import datetime as dt
import json
import re
from pathlib import Path

CONFIG = json.loads(Path(__file__).with_name("sources.json").read_text())
STATUS = re.compile(r"https?://(?:www\.)?(?:twitter|x)\.com/[^/]+/status/(\d+)")


def key(url):
    match = STATUS.match(url)
    return match[1] if match else url.rstrip("/")


def excerpt(text, limit):
    return " ".join(text.split())[:limit]


def section(directory, candidates, excluded, now):
    cutoff = now - dt.timedelta(hours=24)
    lines = ["## 최근 24시간 당사자 원문 · GPT", ""]
    path = directory / "gpt-primary-sources.json"
    snapshot = {}
    try:
        snapshot = json.loads(path.read_text())
    except (OSError, ValueError):
        lines.append("Mac 수집 결과 미도착 · X 조회 여부를 확인할 수 없음.")
    if snapshot:
        checked = dt.datetime.fromisoformat(snapshot["checked"])
        lines.append("Mac 마지막 조회: " + checked.isoformat(timespec="minutes"))
        if now - checked > dt.timedelta(hours=2):
            lines.append("수집 지연 · 마지막 조회 이후 발언은 미확인.")
        lines.extend(snapshot["warnings"])

    rows = list(snapshot.get("rows", []))
    for r in candidates:
        if r["source"] in CONFIG["existing_blog_sources"] and r.get("published"):
            rows.append(dict(kind="blog", url=r["url"], text=r["title"],
                             author=r["source_name"], published=r["published"]))
    used = {key(url) for url in excluded}
    for kind, label in (("people", "추적 계정의 글·답글"), ("blog", "블로그 원문"),
                        ("discovery", "주제 검색 · 당사자 여부 확인")):
        lines.extend(["", "### " + label, ""])
        count = 0
        for r in sorted(rows, key=lambda r: r.get("published", r.get("day", "")), reverse=True):
            if r["kind"] != kind or key(r["url"]) in used:
                continue
            if "published" in r:
                when = dt.datetime.fromisoformat(r["published"].replace("Z", "+00:00"))
                if not cutoff <= when <= now:
                    continue
                date = when.astimezone(dt.timezone(dt.timedelta(hours=9))).strftime("%m-%d %H:%M KST")
            else:
                if not cutoff.date().isoformat() <= r["day"] <= now.date().isoformat():
                    continue
                date = r["day"] + " · 시각 미상, 24시간 여부 확인 필요"
            used.add(key(r["url"]))
            count += 1
            lines.append(f"- {date} · {r['author']} · {excerpt(r['text'], 260)} {r['url']}")
            for parent in r.get("parents", []):
                lines.append(f"  - 앞선 글: {excerpt(parent['text'], 190)} {parent['url']}")
            if r.get("parent") and not r.get("parents"):
                lines.append("  - 질문 원문 확인 필요: https://x.com/i/status/" + r["parent"])
            if ref := r.get("quoted"):
                lines.append(f"  - 인용 원저자 @{ref['author']} ({ref['published']}): {excerpt(ref['text'], 190)} {ref['url']}")
        if not count:
            lines.append("- 검토할 새 후보 없음.")
    return lines + [""]
