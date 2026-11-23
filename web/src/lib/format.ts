const TZ = 'Asia/Seoul';

const dayFmt = new Intl.DateTimeFormat('ko-KR', { timeZone: TZ, month: 'long', day: 'numeric', weekday: 'long' });
const timeFmt = new Intl.DateTimeFormat('ko-KR', { timeZone: TZ, hour: '2-digit', minute: '2-digit', hour12: false });
const keyFmt = new Intl.DateTimeFormat('en-CA', { timeZone: TZ, year: 'numeric', month: '2-digit', day: '2-digit' });

/** "11월 23일 월요일" */
export const dayLabel = (d: Date) => dayFmt.format(d);

/** "14:05" */
export const timeLabel = (d: Date) => timeFmt.format(d);

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
