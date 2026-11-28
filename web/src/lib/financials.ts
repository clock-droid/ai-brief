// 미국 상장사 분기 실적 숫자. collector/financials.py가 SEC XBRL에서 받아 src/data/financials/<TICKER>.json에 적는다.
// 글은 frontmatter `financials`로 무엇을 그릴지만 가리키고, 숫자는 늘 이 파일에서 온다 (WRITING.md 3-2).

export const FIN_METRICS = [
  'revenue',
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
  const file = byTicker.get(ref.ticker.toUpperCase());
  if (!file) throw new Error(`${where}: ${ref.ticker} 숫자 파일이 없음 — python3 collector/financials.py ${ref.ticker}`);
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

/** 962억 달러 / 15.3억 달러 / -4.2억 달러 / 2.46달러 */
export function finValue(v: number, unit: FinSeries['unit']): string {
  if (unit === 'USD/shares') return `${v.toFixed(2)}달러`;
  const eok = v / 1e8;
  const digits = Math.abs(eok) >= 100 ? 0 : 1;
  return `${eok.toLocaleString('ko-KR', { minimumFractionDigits: digits, maximumFractionDigits: digits })}억 달러`;
}

/** +106% / -27% */
export const finPct = (p: number) => `${p >= 0 ? '+' : ''}${Math.round(p)}%`;
