/**
 * 취향 신호: 주인의 반응(좋아요·싫어요 + 이유)과 읽은 기록(펼침·읽은 시간·원문 클릭·보고 지나침)을 모아
 * 비공개 저장소에 파일로 올린다. 순위표(collector/preferences.py)가 이 파일들을 읽어 관심 점수를 낸다.
 *
 * 토큰이 있는 브라우저에서만 동작한다. 토큰은 /settings/에서 붙여넣고 이 브라우저(localStorage)에만 남는다.
 * 토큰이 없으면 아무것도 기록하지 않는다 (다른 방문자는 추적하지 않는다).
 */

/** 신호를 받는 비공개 저장소. collector/preferences.py의 SIGNALS 경로와 같아야 한다 */
const SIGNAL_REPO = 'clock-droid/ai-brief-taste';
const SIGNAL_DIR = 'signals';
const KEEPALIVE_LIMIT = 60_000;

const KEY = { token: 'aib.token', queue: 'aib.queue', outbox: 'aib.outbox', votes: 'aib.votes', tokenError: 'aib.tokenError' };

export const LIKE_REASONS = ['주제가 좋음', '더 깊게 보고 싶음', '쓸모 있음'] as const;
export const DISLIKE_REASONS = ['관심 없는 주제', '너무 뻔함', '홍보성', '과장'] as const;

export type SignalEvent =
  | { t: 'vote'; id: string; v: 1 | -1 | 0; why: string[] }
  | { t: 'open'; id: string }
  | { t: 'dwell'; id: string; sec: number; depth?: number }
  | { t: 'click'; id: string; url: string }
  | { t: 'seen'; id: string };

type Stamped = SignalEvent & { at: string };
type Batch = { path: string; events: Stamped[] };
export type Vote = { v: 1 | -1; why: string[] };

function read<T>(key: string, fallback: T): T {
  try {
    const raw = localStorage.getItem(key);
    return raw ? (JSON.parse(raw) as T) : fallback;
  } catch {
    return fallback;
  }
}

function write(key: string, value: unknown) {
  try {
    if (value === null) localStorage.removeItem(key);
    else localStorage.setItem(key, typeof value === 'string' ? value : JSON.stringify(value));
  } catch {
    /* 저장소를 못 쓰면 기록을 포기한다 */
  }
}

export function getToken(): string | null {
  try {
    return localStorage.getItem(KEY.token);
  } catch {
    return null;
  }
}

export function setToken(token: string | null) {
  write(KEY.token, token);
  write(KEY.tokenError, null);
}

/** 마지막 전송이 토큰 문제로 실패했으면 그 상태 코드 */
export function tokenError(): number | null {
  return read<number | null>(KEY.tokenError, null);
}

export const enabled = () => !!getToken();

export function record(e: SignalEvent) {
  if (!enabled()) return;
  const queue = read<Stamped[]>(KEY.queue, []);
  queue.push({ ...e, at: new Date().toISOString() });
  write(KEY.queue, queue);
}

/** 이 브라우저에서 누른 반응. 화면에 눌린 상태를 보여 주는 데만 쓴다 (기준 기록은 저장소의 신호 파일) */
export function getVote(id: string): Vote | null {
  return read<Record<string, Vote>>(KEY.votes, {})[id] ?? null;
}

export function setVote(id: string, vote: Vote | null) {
  const votes = read<Record<string, Vote>>(KEY.votes, {});
  if (vote) votes[id] = vote;
  else delete votes[id];
  write(KEY.votes, votes);
  record({ t: 'vote', id, v: vote?.v ?? 0, why: vote?.why ?? [] });
}

function encode(text: string): string {
  const bytes = new TextEncoder().encode(text);
  let bin = '';
  bytes.forEach((b) => (bin += String.fromCharCode(b)));
  return btoa(bin);
}

function batchPath(now: Date): string {
  const iso = now.toISOString(); // 2026-11-25T03:12:45.123Z
  const day = iso.slice(0, 10).replaceAll('-', '/');
  const stamp = iso.slice(0, 19).replaceAll(':', '');
  return `${SIGNAL_DIR}/${day}/${stamp}-${Math.random().toString(36).slice(2, 8)}.json`;
}

/**
 * 쌓인 신호를 파일 하나로 올린다. 페이지를 떠날 때도 끝까지 가도록 keepalive를 쓴다.
 * 큐는 먼저 경로가 정해진 묶음(outbox)으로 옮긴 뒤 보낸다. 응답을 못 받고 페이지가 닫혀도 다음 방문 때
 * 같은 경로로 다시 보내고, 이미 올라가 있으면 GitHub이 422를 돌려주므로 중복 없이 끝난다.
 */
export async function flush() {
  const token = getToken();
  if (!token) return;
  const queue = read<Stamped[]>(KEY.queue, []);
  const outbox = read<Batch[]>(KEY.outbox, []);
  if (queue.length) {
    outbox.push({ path: batchPath(new Date()), events: queue });
    write(KEY.outbox, outbox);
    write(KEY.queue, []);
  }
  for (const batch of outbox) {
    let status = 0;
    const body = JSON.stringify({ message: `신호 ${batch.events.length}개`, content: encode(JSON.stringify(batch.events)) });
    try {
      const res = await fetch(`https://api.github.com/repos/${SIGNAL_REPO}/contents/${batch.path}`, {
        method: 'PUT',
        keepalive: body.length < KEEPALIVE_LIMIT, // 브라우저가 keepalive 본문을 64KB로 제한한다
        headers: { Authorization: `Bearer ${token}`, Accept: 'application/vnd.github+json' },
        body,
      });
      status = res.status;
    } catch {
      return; // 네트워크 실패: 다음 기회에 다시 보낸다
    }
    if (status === 401 || status === 403 || status === 404) {
      write(KEY.tokenError, status); // 토큰 만료·권한 부족. /settings/에 표시
      return;
    }
    if (status === 201 || status === 422) {
      write(KEY.outbox, read<Batch[]>(KEY.outbox, []).filter((b) => b.path !== batch.path));
    }
  }
}
