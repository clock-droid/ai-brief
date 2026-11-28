"""SEC 13F 큰손 포트폴리오 변화.

유명 투자자(sources.json sec_13f의 filers)가 새 13F-HR을 내면 후보 하나를 만들고,
직전 분기와 견줘 신규·추가·축소·청산을 data/13f/<cik>-<접수번호>.json에 적는다 (글쓰기 작업이 읽는다).

- 새 공시 감지: data.sec.gov/submissions/CIK##########.json (일반 UA로 받을 수 있다)
- 보유 내역: www.sec.gov/Archives의 정보표 XML. SEC 공정 접근 규칙상 **연락처를 밝힌 UA가 있어야** 받는다
  (일반 UA는 403). 연락처는 환경 변수 SEC_CONTACT(메일 주소)로만 받고 저장소에 두지 않는다.
  없으면 수집기가 이 출처를 통째로 건너뛰고 경고를 남긴다 (collect.py collect_sec_13f).
- 비교는 (CUSIP, 풋·콜) 단위로 주식 수를 합쳐 한다. 평가액(value, 달러)은 주가에 따라 변하므로 판단에 쓰지 않는다.
- 13F는 분기 말 45일 뒤에 나오고, 미국 상장 롱 포지션만 담는다 (공매도·현금·해외 주식 없음).

조사 근거: research/06-econ-sources.md E절 (2026-11-28 버크셔 2→3분기 비교 시험).
"""
from __future__ import annotations

import collections
import datetime as dt
import gzip
import json
import os
import time
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "data" / "13f"
GENERIC_UA = "ai-brief-collector/0.1"
NS = {"n": "http://www.sec.gov/edgar/document/thirteenf/informationtable"}
FORMS = ("13F-HR", "13F-HR/A")
DELAY_SEC = 0.2  # SEC 상한은 초당 10회


def _get(url: str, ua: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": ua, "Accept-Encoding": "gzip, deflate"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        raw = resp.read()
    time.sleep(DELAY_SEC)
    return gzip.decompress(raw) if raw[:2] == b"\x1f\x8b" else raw


def contact_ua() -> str | None:
    contact = os.environ.get("SEC_CONTACT", "").strip()
    return f"AIBrief {contact}" if "@" in contact else None


def filings(cik: int) -> list[dict]:
    """13F-HR(정정 포함) 접수 목록, 최신순."""
    data = json.loads(_get(f"https://data.sec.gov/submissions/CIK{cik:010d}.json", GENERIC_UA))
    recent = data["filings"]["recent"]
    rows = [
        {"form": f, "accession": a, "filed": fd, "period": rd}
        for f, a, fd, rd in zip(recent["form"], recent["accessionNumber"], recent["filingDate"], recent["reportDate"])
        if f in FORMS
    ]
    return sorted(rows, key=lambda r: r["filed"], reverse=True)


def filing_url(cik: int, accession: str) -> str:
    return f"https://www.sec.gov/Archives/edgar/data/{cik}/{accession.replace('-', '')}/"


def holdings(cik: int, accession: str, ua: str) -> dict[tuple[str, str], dict]:
    base = filing_url(cik, accession)
    index = json.loads(_get(base + "index.json", ua))
    table = None
    for item in index["directory"]["item"]:
        name = item["name"]
        if name.endswith(".xml") and name != "primary_doc.xml":
            body = _get(base + name, ua)
            if b"informationTable" in body:
                table = body
                break
    if table is None:
        raise ValueError(f"정보표 없음: {base}")
    agg: dict[tuple[str, str], dict] = collections.defaultdict(lambda: {"shares": 0, "value": 0, "name": ""})
    for t in ET.fromstring(table).findall("n:infoTable", NS):
        key = (t.findtext("n:cusip", namespaces=NS), t.findtext("n:putCall", default="", namespaces=NS))
        row = agg[key]
        row["shares"] += int(t.findtext("n:shrsOrPrnAmt/n:sshPrnamt", namespaces=NS))
        row["value"] += int(t.findtext("n:value", namespaces=NS))
        row["name"] = t.findtext("n:nameOfIssuer", namespaces=NS)
    return dict(agg)


def compare(new: dict, old: dict) -> list[dict]:
    """신규·추가·축소·청산. 현재 평가액이 큰 순(청산은 직전 평가액 순)."""
    changes = []
    for key in set(new) | set(old):
        n, o = new.get(key), old.get(key)
        ns, os_ = (n or {}).get("shares", 0), (o or {}).get("shares", 0)
        if ns == os_:
            continue
        kind = "신규" if not os_ else "청산" if not ns else "추가" if ns > os_ else "축소"
        changes.append({
            "kind": kind,
            "name": (n or o)["name"],
            "cusip": key[0],
            "put_call": key[1],
            "shares_before": os_,
            "shares_after": ns,
            "change_pct": round((ns - os_) / os_ * 100, 1) if os_ else None,
            "value_after_usd": (n or {}).get("value", 0),
            "value_before_usd": (o or {}).get("value", 0),
        })
    return sorted(changes, key=lambda c: -(c["value_after_usd"] or c["value_before_usd"]))


def previous_period(rows: list[dict], period: str) -> dict | None:
    """직전 분기의 최신 접수 (정정이 있으면 정정본)."""
    older = [r for r in rows if r["period"] < period]
    if not older:
        return None
    prev_period = max(r["period"] for r in older)
    return next(r for r in rows if r["period"] == prev_period)


def report(filer: dict, current: dict, rows: list[dict], ua: str) -> dict:
    """data/13f/에 남길 비교 결과."""
    out = {
        "filer": filer["name"],
        "manager": filer.get("manager", ""),
        "cik": filer["cik"],
        "form": current["form"],
        "accession": current["accession"],
        "filed": current["filed"],
        "period": current["period"],
        "url": filing_url(filer["cik"], current["accession"]),
    }
    prev = previous_period(rows, current["period"])
    if prev is None:
        out["changes"] = None
        out["note"] = "직전 분기 공시 없음"
        return out
    new = holdings(filer["cik"], current["accession"], ua)
    old = holdings(filer["cik"], prev["accession"], ua)
    out.update({
        "previous": {"accession": prev["accession"], "period": prev["period"], "filed": prev["filed"]},
        "positions": len(new),
        "positions_before": len(old),
        "total_value_usd": sum(v["value"] for v in new.values()),
        "total_value_before_usd": sum(v["value"] for v in old.values()),
        "changes": compare(new, old),
    })
    return out


def summary_line(rep: dict) -> str:
    if not rep.get("changes"):
        return f"{rep['period']} 기준 13F. {rep.get('note', '')}".strip()
    counts = collections.Counter(c["kind"] for c in rep["changes"])
    top = "; ".join(
        f"{c['kind']} {c['name']}" + (f" {c['change_pct']:+.0f}%" if c["change_pct"] is not None else "")
        for c in rep["changes"][:6]
    )
    tally = " · ".join(f"{k} {counts[k]}" for k in ("신규", "추가", "축소", "청산") if counts[k])
    return f"{rep['period']} 기준, 직전 분기 대비 {tally}. 평가액 큰 순: {top}"


def save(rep: dict) -> Path:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / f"{rep['cik']}-{rep['accession']}.json"
    path.write_text(json.dumps(rep, ensure_ascii=False, indent=1))
    return path


def parse_day(s: str) -> dt.datetime:
    return dt.datetime.strptime(s, "%Y-%m-%d").replace(tzinfo=dt.timezone.utc)
