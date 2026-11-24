import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';
import { CATEGORY_KEYS } from './categories';

// published: 원문 발표 시각 (후보의 published). 카드 위 시각 줄에 "원문 …"으로 표시된다.
const source = z.object({ name: z.string(), url: z.url(), published: z.coerce.date().optional() });

// 속보 카드: 짧은 글. 본문은 ▶ 줄 · 한 줄 요약 · ※ 단서 (WRITING.md 참고).
const cards = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/cards' }),
  schema: z.object({
    title: z.string().max(60),
    date: z.coerce.date(),
    category: z.enum(CATEGORY_KEYS),
    sources: z.array(source).min(1),
    tweet: z
      .object({ author: z.string(), handle: z.string(), text: z.string(), url: z.url() })
      .optional(),
    post: z.string().optional(), // 같은 사건을 다룬 긴 글의 id
  }),
});

// 긴 글: 해설 · 원문 요약 · 정리.
const posts = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/posts' }),
  schema: z.object({
    title: z.string().max(60),
    date: z.coerce.date(),
    category: z.enum(CATEGORY_KEYS),
    updated: z.coerce.date().optional(), // 연재 정리 글을 갱신한 시각 (WRITING.md 6-4)
    format: z.enum(['해설', '원문 요약', '정리']),
    summary: z.array(z.string()).length(3), // 3줄 요약
    sources: z.array(source).min(1),
  }),
});

export const collections = { cards, posts };
