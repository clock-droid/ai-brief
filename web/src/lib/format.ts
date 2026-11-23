const TZ = 'Asia/Seoul';

const dayFmt = new Intl.DateTimeFormat('ko-KR', { timeZone: TZ, month: 'long', day: 'numeric', weekday: 'long' });
const timeFmt = new Intl.DateTimeFormat('ko-KR', { timeZone: TZ, hour: '2-digit', minute: '2-digit', hour12: false });
const keyFmt = new Intl.DateTimeFormat('en-CA', { timeZone: TZ, year: 'numeric', month: '2-digit', day: '2-digit' });

/** "11월 23일 월요일" */
export const dayLabel = (d: Date) => dayFmt.format(d);

/** "14:05" */
export const timeLabel = (d: Date) => timeFmt.format(d);

const shortDayFmt = new Intl.DateTimeFormat('ko-KR', { timeZone: TZ, month: 'long', day: 'numeric' });

/** "11월 22일 18:05" */
export const dateTimeLabel = (d: Date) => `${shortDayFmt.format(d)} ${timeFmt.format(d)}`;

/** X 게시물 id(snowflake)에 들어 있는 게시 시각 */
export function tweetTime(url: string): Date | undefined {
  const id = url.match(/\/status\/(\d{15,20})/)?.[1];
  if (!id) return undefined;
  return new Date(Number((BigInt(id) >> 22n) + 1288834974657n));
}

/** 카드 출처 중 가장 이른 원문 시각. 트윗은 id에서 시각을 읽는다. */
export function earliestSourceTime(sources: { published?: Date }[], tweetUrl?: string): Date | undefined {
  const times = sources.map((s) => s.published).filter((d): d is Date => d instanceof Date);
  const t = tweetUrl ? tweetTime(tweetUrl) : undefined;
  if (t) times.push(t);
  return times.length ? new Date(Math.min(...times.map((d) => d.getTime()))) : undefined;
}

/** KST 기준 날짜 키 "2026-11-23" — 날짜 묶음용 */
export const dayKey = (d: Date) => keyFmt.format(d);

/** 같은 KST 날짜끼리 묶는다. 입력은 최신순이어야 한다. */
export function groupByDay<T extends { data: { date: Date } }>(entries: T[]) {
  const groups: { key: string; label: string; items: T[] }[] = [];
  for (const entry of entries) {
    const key = dayKey(entry.data.date);
    const last = groups.at(-1);
    if (last?.key === key) last.items.push(entry);
    else groups.push({ key, label: dayLabel(entry.data.date), items: [entry] });
  }
  return groups;
}

/** base 경로를 붙인 내부 링크 */
export const href = (path: string) => `${import.meta.env.BASE_URL.replace(/\/$/, '')}${path}`;
