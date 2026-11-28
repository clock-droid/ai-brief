// 미국 상장사 분기 실적 숫자. collector/financials.py가 SEC XBRL에서 받아 src/data/financials/<TICKER>.json에 적는다.
// 글은 frontmatter `financials`로 무엇을 그릴지만 가리키고, 숫자는 늘 이 파일에서 온다 (WRITING.md 3-2).

export const FIN_METRICS = [
  'revenue',
  'cost_of_revenue',
  'gross_profit',
  'operating_income',
  'net_income',
  'rnd',
  'operating_cash_flow',
  'capex',
  'free_cash_flow',
  'eps_diluted',
] as const;
export type FinMetric = (typeof FIN_METRICS)[number];

export const FIN_QUARTERS_SHOWN = 8; // 두 해치: 전년 같은 분기와 바로 견줄 수 있는 가장 짧은 폭

export interface FinQuarter {
  start: string;
  end: string;
  value: number;
  fy: number;
  fq: number;
  form: string;
  filed: string;
  derived: boolean;
}

interface FinFile {
  ticker: string;
  name: string;
  fiscal_year_end_month: number;
  filings_url: string;
  earnings_release_pending: string | null;
  metrics: Partial<Record<FinMetric, { label: string; unit: 'USD' | 'USD/shares'; quarters: FinQuarter[] }>>;
}

const files = import.meta.glob<FinFile>('../data/financials/*.json', { eager: true, import: 'default' });
const byTicker = new Map(Object.values(files).map((f) => [f.ticker, f]));

/** 그림의 한 칸. 값이 공시되지 않은 분기(주당순이익의 4분기 등)도 칸은 남겨 빈 분기를 숨기지 않는다 */
export interface FinSlot {
  fy: number;
  fq: number;
  q?: FinQuarter;
}

export interface FinSeries {
  key: FinMetric;
  label: string;
  unit: 'USD' | 'USD/shares';
  slots: FinSlot[];
  /** 마지막 분기와 전년 같은 분기의 증감(%). 전년 값이 0 이하이면 비율이 뜻이 없어 비운다 */
  yoy?: number;
}

export interface FinChartData {
  ticker: string;
  name: string;
  fyeMonth: number;
  filingsUrl: string;
  series: FinSeries[];
  anyDerived: boolean;
  anyMissing: boolean;
  /** 그림의 마지막 분기가 받은 숫자 중 최신이고, 그 뒤 실적 발표(8-K)가 이미 나와 있다 */
  newerQuarterPending: boolean;
}

/** 글이 가리킨 회사·항목·마지막 분기로 그릴 숫자를 고른다. 없으면 빌드를 멈춘다 (숫자를 지어내지 않게). */
export function finChartData(ref: { ticker: string; metrics: FinMetric[]; through: Date }, where: string): FinChartData {
  const file = fileOf(ref.ticker, where);
  const through = ref.through.toISOString().slice(0, 10);
  let latestEnd = '';
  const series = ref.metrics.map((key) => {
    const m = file.metrics[key];
    if (!m) throw new Error(`${where}: ${ref.ticker}에 ${key} 숫자가 없음`);
    const all = m.quarters;
    latestEnd = all.at(-1)!.end > latestEnd ? all.at(-1)!.end : latestEnd;
    const upto = all.filter((q) => q.end <= through);
    if (upto.at(-1)?.end !== through) {
      throw new Error(`${where}: ${ref.ticker} ${key}에 ${through}로 끝나는 분기가 없음 — through를 스크립트가 알려 준 날짜로`);
    }
    const last = upto.at(-1)!;
    const slots: FinSlot[] = [];
    for (let i = FIN_QUARTERS_SHOWN - 1; i >= 0; i--) {
      const n = last.fy * 4 + (last.fq - 1) - i;
      const fy = Math.floor(n / 4);
      const fq = (n % 4) + 1;
      slots.push({ fy, fq, q: upto.find((q) => q.fy === fy && q.fq === fq) });
    }
    const prior = all.find((q) => q.fy === last.fy - 1 && q.fq === last.fq);
    const yoy = prior && prior.value > 0 ? (last.value / prior.value - 1) * 100 : undefined;
    return { key, label: m.label, unit: m.unit, slots, yoy };
  });
  return {
    ticker: file.ticker,
    name: file.name,
    fyeMonth: file.fiscal_year_end_month,
    filingsUrl: file.filings_url,
    series,
    anyDerived: series.some((s) => s.slots.some((x) => x.q?.derived)),
    anyMissing: series.some((s) => s.slots.some((x) => !x.q)),
    newerQuarterPending: Boolean(file.earnings_release_pending) && through === latestEnd,
  };
}

export interface FinCompany {
  ticker: string;
  name: string; // 글에 쓰는 우리말 이름
}

const fileOf = (ticker: string, where: string) => {
  const file = byTicker.get(ticker.toUpperCase());
  if (!file) throw new Error(`${where}: ${ticker} 숫자 파일이 없음 — python3 collector/financials.py ${ticker}`);
  return file;
};

/** 다른 회사의 '같은 분기': 결산월이 달라 끝 날짜가 어긋나므로, 기준 분기 끝과 45일 안에서 가장 가까운 분기 */
function nearestQuarter(quarters: FinQuarter[], end: string): FinQuarter | undefined {
  const t = Date.parse(end);
  let best: FinQuarter | undefined;
  for (const q of quarters) {
    const d = Math.abs(Date.parse(q.end) - t);
    if (d <= 45 * 86400e3 && (!best || d < Math.abs(Date.parse(best.end) - t))) best = q;
  }
  return best;
}

/** 분기 끝 날짜의 달. 52·53주 결산(1월 26일, 2월 1일)은 가까운 월말로 읽는다 */
function endMonth(end: string): number {
  const d = new Date(`${end}T00:00:00Z`);
  if (d.getUTCDate() <= 7) d.setUTCDate(0);
  return d.getUTCMonth() + 1;
}

/** 기준 회사와 분기 끝 달이 다를 때만 "7월 말"을 붙인다 */
const offLabel = (end: string, subjectEnd: string) =>
  endMonth(end) === endMonth(subjectEnd) ? undefined : `${endMonth(end)}월 말`;

export interface FinPeerRow extends FinCompany {
  value: number;
  end: string;
  subject: boolean;
  /** 기준 회사와 분기 끝 달이 다르면 "7월 말" */
  offLabel?: string;
}

export interface FinPeerChart {
  key: FinMetric;
  rows: FinPeerRow[]; // 값이 큰 순
  missing: string[]; // 이 항목을 따로 공시하지 않은 회사 이름
}

/** 항목마다 기준 회사와 경쟁사의 같은 분기 값을 나란히 */
export function finPeers(
  subject: FinCompany,
  peers: FinCompany[],
  metrics: FinMetric[],
  through: Date,
  where: string,
): FinPeerChart[] {
  const end = through.toISOString().slice(0, 10);
  return metrics.map((key) => {
    const rows: FinPeerRow[] = [];
    const missing: string[] = [];
    for (const c of [subject, ...peers]) {
      const q = nearestQuarter(fileOf(c.ticker, where).metrics[key]?.quarters ?? [], end);
      if (!q) {
        missing.push(c.name);
        continue;
      }
      rows.push({ ...c, value: q.value, end: q.end, subject: c === subject, offLabel: offLabel(q.end, end) });
    }
    rows.sort((a, b) => b.value - a.value);
    return { key, rows, missing };
  });
}

export const FIN_SPLIT_PARTS = [
  { key: 'cost', label: '매출원가' },
  { key: 'rnd', label: '연구개발비' },
  { key: 'other', label: '그 밖의 비용' },
  { key: 'profit', label: '영업이익' },
] as const;
export type FinSplitKey = (typeof FIN_SPLIT_PARTS)[number]['key'];

export interface FinSplitRow extends FinCompany {
  /** 매출 100원 중 몇 원. 영업손실이면 profit은 음수, 비용 합은 100을 넘는다 */
  parts: Record<FinSplitKey, number>;
  rndFolded: boolean; // 연구개발비를 따로 공시하지 않아 '그 밖의 비용'에 들어감
  end: string;
  subject: boolean;
  offLabel?: string;
}

/** 매출 100원이 원가·연구개발·그 밖의 비용·영업이익으로 어떻게 나뉘나. 그 밖의 비용 = 매출 - 원가 - 연구개발비 - 영업이익 */
export function finSplit(subject: FinCompany, peers: FinCompany[], through: Date, where: string): FinSplitRow[] {
  const end = through.toISOString().slice(0, 10);
  const rows: FinSplitRow[] = [];
  for (const c of [subject, ...peers]) {
    const m = fileOf(c.ticker, where).metrics;
    const rev = nearestQuarter(m.revenue?.quarters ?? [], end);
    const at = (k: FinMetric) => (rev ? m[k]?.quarters.find((q) => q.end === rev.end)?.value : undefined);
    const cost = at('cost_of_revenue');
    const op = at('operating_income');
    if (!rev || rev.value <= 0 || cost === undefined || op === undefined) {
      if (c === subject) throw new Error(`${where}: ${c.ticker}는 매출·매출원가·영업이익이 다 있어야 100원 쪼개기를 그린다`);
      continue;
    }
    const rnd = at('rnd');
    const per = (v: number) => (v / rev.value) * 100;
    const parts = {
      cost: per(cost),
      rnd: rnd === undefined ? 0 : per(rnd),
      other: per(rev.value - cost - (rnd ?? 0) - op),
      profit: per(op),
    };
    rows.push({ ...c, parts, rndFolded: rnd === undefined, end: rev.end, subject: c === subject, offLabel: offLabel(rev.end, end) });
  }
  return rows;
}

/** 962억 달러 / 15.3억 달러 / -4.2억 달러 / 2.46달러 */
export function finValue(v: number, unit: FinSeries['unit']): string {
  if (unit === 'USD/shares') return `${v.toFixed(2)}달러`;
  const eok = v / 1e8;
  const digits = Math.abs(eok) >= 100 ? 0 : 1;
  return `${eok.toLocaleString('ko-KR', { minimumFractionDigits: digits, maximumFractionDigits: digits })}억 달러`;
}

/** +106% / -27% */
export const finPct = (p: number) => `${p >= 0 ? '+' : ''}${Math.round(p)}%`;
