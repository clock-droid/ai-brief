"""미국 상장사 분기 실적 숫자 (SEC XBRL) → 사이트의 '숫자 그림'.

글 쓰는 쪽이 숫자를 손으로 옮기지 않게, 공시 원본에서 바로 받아 web/src/data/financials/<TICKER>.json에 적는다.
사이트(FinancialChart.astro)가 이 파일로 그림을 그리고, 글 frontmatter의 `financials`는 무엇을 그릴지만 가리킨다 (WRITING.md 3-2).

    python3 collector/financials.py NVDA            # 받고 요약 + 붙여 넣을 frontmatter 출력
    python3 collector/financials.py NVDA MSFT GOOGL # 여러 회사

- 출처: data.sec.gov/api/xbrl/companyfacts (10-Q·10-K에 붙은 XBRL), data.sec.gov/submissions (결산월·최근 공시).
  둘 다 일반 UA로 받는다 (연락처 UA가 필요한 www.sec.gov는 쓰지 않는다). 티커→CIK는 EDGAR 회사 검색(efts)으로.
- 분기 숫자 만들기:
  · 손익 항목은 10-Q에 3개월치가 있다 → 그대로 쓴다.
  · 현금흐름은 10-Q에 누적(연초부터)만 있고, 4분기는 어느 항목이든 10-K의 연간만 있다
    → 같은 시작일의 누적에서 직전 누적을 빼서 만든다 (derived: true).
  · 주당순이익은 빼기로 만들면 주식 수 변화 때문에 틀린다 → 공시된 3개월치만 쓰고, 없는 분기는 비운다.
    주식 분할이 있으면 전년 같은 분기만 새 기준으로 고쳐 공시되므로 8개 분기 안에 분할 전후 값이 섞일 수 있다.
  · 회사가 중간에 XBRL 항목 이름을 바꾸는 일이 흔해서(엔비디아 설비투자 등) 항목별 후보 이름을 여러 개 두고,
    최근 숫자가 있는 이름부터 분기를 채운다.
  · 같은 기간 숫자가 여러 공시에 있으면(다음 해 비교 수치·정정) 가장 늦게 접수된 것을 쓴다.
- 상장 서류(S-1)에는 XBRL 재무 숫자가 없어 갓 상장한 회사는 첫 10-Q가 나온 뒤부터 된다.
- 한계: 실적 발표(보도자료, 8-K)에는 XBRL 재무 숫자가 없다. 발표 당일엔 그 분기가 아직 없고, 10-Q·10-K가 나와야 들어온다.
  스크립트가 이 경우를 알려 준다.
"""
from __future__ import annotations

import argparse
import datetime as dt
import gzip
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "web" / "src" / "data" / "financials"
UA = "ai-brief-collector/0.1"
DELAY_SEC = 0.2  # SEC 상한은 초당 10회
FORMS = {"10-Q", "10-K", "10-Q/A", "10-K/A", "20-F", "40-F"}
KEEP_QUARTERS = 12  # 처음 받을 때 남기는 분기 수. 다시 받을 땐 예전 분기를 지우지 않는다 (merge_previous)

# key: (한국어 이름, XBRL 후보 이름들, 단위, 종류). 종류 flow = 기간 합계(빼기로 분기 계산 가능), per_share = 3개월치만.
METRICS: dict[str, tuple[str, list[str], str, str]] = {
    "revenue": (
        "매출",
        [
            "Revenues",
            "RevenueFromContractWithCustomerExcludingAssessedTax",
            "RevenueFromContractWithCustomerIncludingAssessedTax",
            "SalesRevenueNet",
        ],
        "USD",
        "flow",
    ),
    "cost_of_revenue": ("매출원가", ["CostOfRevenue", "CostOfGoodsAndServicesSold"], "USD", "flow"),
    "gross_profit": ("매출총이익", ["GrossProfit"], "USD", "flow"),
    "operating_income": ("영업이익", ["OperatingIncomeLoss"], "USD", "flow"),
    "net_income": ("순이익", ["NetIncomeLoss"], "USD", "flow"),
    "rnd": ("연구개발비", ["ResearchAndDevelopmentExpense"], "USD", "flow"),
    "operating_cash_flow": ("영업활동 현금흐름", ["NetCashProvidedByUsedInOperatingActivities"], "USD", "flow"),
    "capex": (
        "설비투자",
        ["PaymentsToAcquirePropertyPlantAndEquipment", "PaymentsToAcquireProductiveAssets"],
        "USD",
        "flow",
    ),
    "eps_diluted": ("희석 주당순이익", ["EarningsPerShareDiluted"], "USD/shares", "per_share"),
}
# 다른 항목에서 계산하는 것: 잉여현금흐름 = 영업활동 현금흐름 - 설비투자 (같은 분기 둘 다 있을 때만)
DERIVED = {"free_cash_flow": "잉여현금흐름"}


def _get_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Encoding": "gzip, deflate"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        raw = resp.read()
    time.sleep(DELAY_SEC)
    return json.loads(gzip.decompress(raw) if raw[:2] == b"\x1f\x8b" else raw)


def resolve_cik(ticker: str) -> int:
    q = urllib.parse.quote(ticker)
    hits = _get_json(f"https://efts.sec.gov/LATEST/search-index?keysTyped={q}")["hits"]["hits"]
    for h in hits:
        tickers = [t.strip().upper() for t in h["_source"].get("tickers", "").split(",")]
        if ticker.upper() in tickers:
            return int(h["_id"])
    raise SystemExit(f"{ticker}: EDGAR에서 이 티커를 못 찾음 (미국 상장사가 아니거나 티커가 다름)")


def _date(s: str) -> dt.date:
    return dt.date.fromisoformat(s)


def _days(start: str, end: str) -> int:
    return (_date(end) - _date(start)).days + 1


def _is_quarter(days: int) -> bool:
    return 80 <= days <= 100


def _period_facts(facts: dict, concept: str, unit: str) -> dict[tuple[str, str], dict]:
    """(시작, 끝) → 가장 늦게 접수된 사실. 10-Q·10-K 계열만, 시작일이 있는 기간 값만."""
    out: dict[tuple[str, str], dict] = {}
    for f in facts.get(concept, {}).get("units", {}).get(unit, []):
        if f.get("form") not in FORMS or "start" not in f:
            continue
        key = (f["start"], f["end"])
        if key not in out or f["filed"] > out[key]["filed"]:
            out[key] = f
    return out


def _quarters_from(periods: dict[tuple[str, str], dict], kind: str) -> dict[str, dict]:
    """끝 날짜 → 분기 값. 3개월치는 그대로, flow는 누적끼리 빼서 빈 분기를 만든다."""
    q: dict[str, dict] = {}
    for (start, end), f in periods.items():
        if _is_quarter(_days(start, end)):
            q[end] = {"start": start, "end": end, "value": f["val"], "form": f["form"], "filed": f["filed"],
                      "accn": f["accn"], "derived": False}
    if kind != "flow":
        return q
    by_start: dict[str, list[tuple[str, dict]]] = {}
    for (start, end), f in periods.items():
        if _days(start, end) <= 380:
            by_start.setdefault(start, []).append((end, f))
    for start, rows in by_start.items():
        rows.sort()
        for (prev_end, prev), (end, cur) in zip(rows, rows[1:]):
            if end in q:
                continue
            gap = (_date(end) - _date(prev_end)).days
            if _is_quarter(gap):
                q[end] = {
                    "start": (_date(prev_end) + dt.timedelta(days=1)).isoformat(),
                    "end": end,
                    "value": cur["val"] - prev["val"],
                    "form": cur["form"],
                    "filed": cur["filed"],
                    "accn": cur["accn"],
                    "derived": True,
                }
    return q


def _round_month(d: dt.date) -> tuple[int, int]:
    """52·53주 회계연도는 월말이 아닌 날(1월 26일, 2월 1일)에 끝난다 → 가까운 월말의 (연, 월)."""
    if d.day <= 7:
        d = d.replace(day=1) - dt.timedelta(days=1)
    return d.year, d.month


def fiscal_label(end: str, fye_month: int) -> tuple[int, int]:
    """분기 끝 날짜 → (회계연도, 분기). 회계연도는 그 해가 끝나는 달력 연도로 부른다 (엔비디아 2026년 1월 말 결산 = FY2026)."""
    y, m = _round_month(_date(end))
    months_after = (m - fye_month) % 12
    fq = 4 if months_after == 0 else (months_after + 2) // 3
    fy = y if m <= fye_month else y + 1
    return fy, fq


def build(ticker: str) -> dict:
    ticker = ticker.upper()
    cik = resolve_cik(ticker)
    sub = _get_json(f"https://data.sec.gov/submissions/CIK{cik:010d}.json")
    facts_doc = _get_json(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json")
    gaap = facts_doc.get("facts", {}).get("us-gaap", {})
    fye_month = int(sub["fiscalYearEnd"][:2])

    metrics: dict[str, dict] = {}
    for key, (label, concepts, unit, kind) in METRICS.items():
        per_concept = []
        for c in concepts:
            q = _quarters_from(_period_facts(gaap, c, unit), kind)
            if q:
                per_concept.append((max(q), c, q))
        if not per_concept:
            continue
        merged: dict[str, dict] = {}
        used: list[str] = []
        for _, c, q in sorted(per_concept, reverse=True):  # 최근 숫자가 있는 이름부터
            added = False
            for end, row in q.items():
                if end not in merged:
                    merged[end] = {**row, "concept": c}
                    added = True
            if added:
                used.append(c)
        metrics[key] = {"label": label, "unit": unit, "concepts": used, "quarters": merged}

    if "operating_cash_flow" in metrics and "capex" in metrics:
        ocf, capex = metrics["operating_cash_flow"]["quarters"], metrics["capex"]["quarters"]
        fcf = {
            end: {**ocf[end], "value": ocf[end]["value"] - capex[end]["value"], "concept": "영업활동 현금흐름 - 설비투자",
                  "derived": True}
            for end in ocf
            if end in capex
        }
        metrics["free_cash_flow"] = {"label": DERIVED["free_cash_flow"], "unit": "USD",
                                     "concepts": ["operating_cash_flow - capex"], "quarters": fcf}

    for m in metrics.values():
        rows = sorted(m["quarters"].values(), key=lambda r: r["end"])[-KEEP_QUARTERS:]
        for r in rows:
            r["fy"], r["fq"] = fiscal_label(r["end"], fye_month)
        m["quarters"] = rows

    recent = sub["filings"]["recent"]
    filings = list(zip(recent["form"], recent["filingDate"], recent["reportDate"], recent.get("items", [""] * len(recent["form"]))))
    latest_report = next(((f, fd, rd) for f, fd, rd, _ in filings if f in FORMS), None)
    earnings_8k = next((fd for f, fd, _, items in filings if f == "8-K" and "2.02" in (items or "")), None)
    pending = None
    if latest_report and earnings_8k and earnings_8k > latest_report[1]:
        pending = earnings_8k

    return {
        "ticker": ticker,
        "cik": cik,
        "name": sub.get("name") or facts_doc.get("entityName"),
        "fiscal_year_end_month": fye_month,
        "fetched": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
        "filings_url": f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik:010d}&type=10-&dateb=&owner=include&count=40",
        "latest_report": {"form": latest_report[0], "filed": latest_report[1], "period": latest_report[2]} if latest_report else None,
        "earnings_release_pending": pending,
        "metrics": metrics,
    }


def _fmt(v: float, unit: str) -> str:
    if unit == "USD/shares":
        return f"{v:.2f}달러"
    eok = v / 1e8
    return f"{eok:,.0f}억 달러" if abs(eok) >= 100 else f"{eok:,.1f}억 달러"


def report(doc: dict) -> str:
    lines = [f"{doc['ticker']} {doc['name']} — 결산월 {doc['fiscal_year_end_month']}월, 최신 정식 공시 "
             f"{doc['latest_report']['form']} {doc['latest_report']['filed']} ({doc['latest_report']['period']} 기준)"]
    if doc["earnings_release_pending"]:
        lines.append(f"  ! {doc['earnings_release_pending']}에 실적 발표(8-K 2.02)가 나왔지만 아직 10-Q·10-K 전이라 "
                     "그 분기 숫자는 없다. 그림 설명에 자동으로 붙는다.")
    for key, m in doc["metrics"].items():
        if not m["quarters"]:
            continue
        last = m["quarters"][-1]
        yoy = next((r for r in m["quarters"] if r["fy"] == last["fy"] - 1 and r["fq"] == last["fq"]), None)
        change = ""
        if yoy and yoy["value"] > 0:
            change = f", 전년 같은 분기 대비 {(last['value'] / yoy['value'] - 1) * 100:+.0f}%"
        lines.append(f"  {key:20s} {m['label']}: FY{last['fy']} {last['fq']}분기 {_fmt(last['value'], m['unit'])}{change}"
                     f" ({len(m['quarters'])}개 분기)")
    last_end = max((m["quarters"][-1]["end"] for m in doc["metrics"].values() if m["quarters"]), default=None)
    lines += ["", "frontmatter에 붙일 것 (metrics는 위 key에서 1~3개, through는 글이 다루는 마지막 분기 끝 날짜):",
              "financials:", f"  ticker: {doc['ticker']}", "  metrics: [revenue, operating_income]", f"  through: {last_end}"]
    return "\n".join(lines)


def merge_previous(doc: dict, path: Path) -> None:
    """다시 받을 때 예전 파일의 분기를 남긴다. 예전 글은 frontmatter through로 그 시점 8개 분기를 그리므로,
    파일이 최근 12개 분기로 잘리면 몇 분기 뒤 예전 글의 그림이 비거나 빌드가 멈춘다. 같은 분기는 새 값(정정 반영)을 쓴다."""
    if not path.exists():
        return
    old = json.loads(path.read_text())
    for key, m in doc["metrics"].items():
        new_ends = {r["end"] for r in m["quarters"]}
        kept = [r for r in old.get("metrics", {}).get(key, {}).get("quarters", []) if r["end"] not in new_ends]
        m["quarters"] = sorted(kept + m["quarters"], key=lambda r: r["end"])


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("tickers", nargs="+")
    args = ap.parse_args()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for t in args.tickers:
        doc = build(t)
        if not doc["metrics"]:
            print(f"{t}: us-gaap 재무 숫자가 없음 (외국 회사의 IFRS 공시 등). 숫자 그림을 붙이지 않는다.", file=sys.stderr)
            continue
        path = OUT_DIR / f"{doc['ticker']}.json"
        merge_previous(doc, path)
        path.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n")
        print(report(doc))
        print(f"→ {path.relative_to(ROOT)}\n")


if __name__ == "__main__":
    main()
