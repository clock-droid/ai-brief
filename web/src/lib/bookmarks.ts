const KEY = 'ai-brief:bookmarks';

export interface Bookmark {
  id: string;
  title: string;
}

export function readBookmarks(): Bookmark[] {
  try {
    const items: unknown = JSON.parse(localStorage.getItem(KEY) ?? '[]');
    if (Array.isArray(items)) {
      return items.filter((item): item is Bookmark =>
        typeof item?.id === 'string' && /^(cards|posts)\/[^/]+$/.test(item.id) &&
        typeof item.title === 'string',
      );
    }
  } catch {
    // Ignore unavailable or unreadable storage.
  }
  return [];
}

/** Returns the saved list, or null if the browser rejected the change. */
export function writeBookmarks(items: Bookmark[]): Bookmark[] | null {
  try {
    localStorage.setItem(KEY, JSON.stringify(items));
    return items;
  } catch {
    return null;
  }
}
