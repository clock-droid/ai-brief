"""Capture public-source candidates on the Mac into the existing private handoff."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import urljoin

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import collect

CONFIG = json.loads((HERE / "sources.json").read_text())
SNAPSHOT = "gpt-primary-sources.json"
SEARCH_INTERVAL = dt.timedelta(hours=3)
SEARCH_PAUSE = dt.timedelta(days=1)


def timestamp(value):
    return dt.datetime.fromisoformat(value.replace("Z", "+00:00"))


class XRateLimit(Exception):
    pass


def read_x(request):
    executable = shutil.which("aside") or str(Path.home() / ".local/bin/aside")
    script = "const input = " + json.dumps(request) + ";\n" + (HERE / "x.js").read_text()
    proc = subprocess.run([executable, "repl", script], capture_output=True, text=True, timeout=125)
    lines = proc.stdout.splitlines()
    ends = [line for line in lines if line.startswith("END ")]
    if re.search(r"HTTP 429\b", proc.stderr + "\n" + "\n".join(l for l in lines if not l.startswith("ROW "))):
        raise XRateLimit
    if proc.returncode or not ends:
        raise RuntimeError(f"Aside 응답 미완료 (exit={proc.returncode})")
    return [json.loads(line[4:]) for line in lines if line.startswith("ROW ")], ends[-1] == "END true"


def schmid_index(start, end):
    # The index exposes calendar dates only. Preserve this precision for the editor.
    # Read the machine-readable <time dateTime> rather than the display text around it.
    base = "https://www.philschmid.de/"
    html = collect.fetch(base)
    pattern = r'<a href="(/[^"#?]+)"><article\b.*?<h3[^>]*>(.*?)</h3>.*?<time [^>]*dateTime="(\d{4}-\d{2}-\d{2})"'
    entries = re.findall(pattern, html, re.S)
    if not entries:
        raise ValueError("블로그 목록 형식 변경")
    for path, title, date in entries:
        day = dt.date.fromisoformat(date)
        if start.date() <= day <= end.date():
            yield dict(url=urljoin(base, path), author="Philipp Schmid", text=collect.clean_text(title),
                       day=day.isoformat(), kind="blog")



def public_rows(rows, previously_public, warnings):
    # The discovery session is signed in. Only carry publicly embeddable posts
    # (including quoted material and parent context) into the private Git handoff.
    refs = {}
    for row in rows:
        for ref in [row, *row.get("parents", []), row.get("quoted")]:
            if ref and "id" in ref:
                refs[ref["id"]] = ref["url"]
    public = set(previously_public).intersection(refs)
    pending = sorted(refs.keys() - public)

    def readable(status_id):
        result = collect.oembed(refs[status_id])
        return bool(result and result.get("author"))

    with ThreadPoolExecutor(max_workers=6) as pool:
        public.update(i for i, ok in zip(pending, pool.map(readable, pending)) if ok)
    if len(public) < len(refs):
        warnings.append(f"공개 원문을 확인하지 못한 X 링크 {len(refs) - len(public)}개 제외")
    result = []
    for row in rows:
        if "id" in row and row["id"] not in public:
            continue
        if row.get("quoted") and row["quoted"]["id"] not in public:
            row.pop("quoted")
        if "parents" in row:
            verified = []
            for parent in row["parents"]:
                if parent["id"] not in public:
                    break
                verified.append(parent)
            row["parents"] = verified
        result.append(row)
    return result, sorted(public)


def capture(directory):
    now = dt.datetime.now(dt.timezone.utc)
    start = now - dt.timedelta(hours=24)
    path = directory / SNAPSHOT
    previous = json.loads(path.read_text()) if path.exists() else {}
    def recent(row):
        if "day" in row:
            return start.date().isoformat() <= row["day"] <= now.date().isoformat()
        return start <= timestamp(row["published"]) <= now
    rows = {r["url"]: r for r in previous.get("rows", []) if recent(r)}
    cursors = previous.get("last_complete", {})
    warnings = []
    # People come from each account's Posts tab, which does not depend on X search.
    # Search is only for the discovery queries: it is throttled, and one failure pauses it
    # for a day so a restricted account is not hammered every hour.
    search_state = previous.get("search", {})
    paused_until = search_state.get("paused_until")
    search_open = not paused_until or now >= timestamp(paused_until)
    if not search_open:
        warnings.append(f"X 검색 일시 중지 중 · {paused_until}까지")
    last_search = search_state.get("last_attempt")
    search_due = search_open and (not last_search or now - timestamp(last_search) >= SEARCH_INTERVAL)
    groups = [("people", handle) for handle in CONFIG["accounts"]]
    if search_due:
        groups.extend(("discovery", q) for q in CONFIG["discovery"])
        search_state["last_attempt"] = now.isoformat()
    groups.sort(key=lambda pair: cursors.get(pair[1], ""))
    rate_limited = False
    for index, (kind, key) in enumerate(groups):
        if kind == "discovery" and not search_open:
            continue
        since = start
        if key in cursors:
            last = timestamp(cursors[key])
            if now - last < dt.timedelta(minutes=10):
                continue
            since = max(start, last - dt.timedelta(minutes=10))
        if kind == "people":
            request = {"user": key, "since": since.isoformat()}
        else:
            window = since.strftime(" since:%Y-%m-%d_%H:%M:%S_UTC") + now.strftime(" until:%Y-%m-%d_%H:%M:%S_UTC")
            request = {"query": key + " -filter:retweets" + window}
        try:
            batch, complete = read_x(request)
            for row in batch:
                if recent(row):
                    old = rows.get(row["url"], {})
                    row["kind"] = "people" if "people" in (kind, old.get("kind")) else kind
                    rows[row["url"]] = {**old, **row}
            if complete:
                cursors[key] = now.isoformat()
            else:
                warnings.append(f"X 조회 일부만 확인: {key}")
        except XRateLimit:
            rate_limited = True
            warnings.append(f"X 요청 한도(429) · 미완료 조회 {len(groups)-index}개, 다음 회차 재개")
            break
        except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired) as exc:
            if kind == "discovery":
                search_open = False
                search_state["paused_until"] = (now + SEARCH_PAUSE).isoformat()
                warnings.append(f"X 검색 실패, {SEARCH_PAUSE.days}일 중지: {key} ({exc})")
            else:
                warnings.append(f"X 계정 글 조회 실패: {key} ({exc})")

    try:
        for row in schmid_index(start, now):
            rows[row["url"]] = row
    except Exception as exc:
        warnings.append(f"Philipp Schmid 블로그 조회 실패: {exc}")

    # Two parents capture both the follow-up question and the statement it refers to.
    known = {r["id"]: r for r in rows.values() if "id" in r}
    for r in rows.values():
        for ancestor in r.get("parents", []):
            known.setdefault(ancestor["id"], ancestor)
    parents = {r["parent"] for r in rows.values() if r.get("parent")}
    for _ in range(2):
        missing = sorted(parents - known.keys())
        for i in range(0, len(missing) if not rate_limited else 0, 12):
            try:
                batch, _ = read_x({"ids": missing[i:i+12]})
            except XRateLimit:
                rate_limited = True
                warnings.append("X 요청 한도(429) · 남은 앞선 글은 다음 회차에 재조회")
                break
            except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired) as exc:
                warnings.append(f"답글 문맥 조회 실패: {exc}")
                break
            known.update({r["id"]: r for r in batch})
        parents = {known[p]["parent"] for p in parents if p in known and known[p].get("parent")}
    for row in rows.values():
        chain = []
        pid = row.get("parent")
        while pid in known and len(chain) < 2:
            ref = known[pid]
            chain.append({k: ref[k] for k in ("id", "url", "text", "published", "parent")})
            pid = ref.get("parent")
        if row.get("parent"):
            row["parents"] = chain

    verified, public_ids = public_rows(list(rows.values()), previous.get("public_ids", []), warnings)
    snapshot = dict(public_ids=public_ids, checked=now.isoformat(), last_complete=cursors, search=search_state, warnings=warnings, rows=verified)
    directory.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode="w", dir=directory, delete=False) as out:
        json.dump(snapshot, out, ensure_ascii=False)
    os.replace(out.name, path)
    print(f"GPT 원문 후보 {len(verified)}개 · 수집 경고 {len(warnings)}개")
    for warning in warnings:
        print(warning, file=sys.stderr)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path, help="비공개 전달 폴더 또는 로컬 검증 폴더")
    capture(parser.parse_args().directory)
