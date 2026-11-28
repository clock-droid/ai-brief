import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';
import { CATEGORY_KEYS } from './categories';

// published: 원문 발표 시각 (후보의 published). 카드 위 시각 줄에 "원문 …"으로 표시된다.
const source = z.object({ name: z.string(), url: z.url(), published: z.coerce.date().optional() });

// 원문 그림: 원본 주소를 그대로 가리킨다 (복사하지 않음). collector/figures.py로 후보를 뽑는다 (WRITING.md 3-1).
// width·height는 그림이 뜨기 전 자리를 잡아 두는 용도.
const figure = z.object({
  src: z.url(),
  alt: z.string().min(1),
  caption: z.string().min(1), // 그림이 무엇을 보여주는지
  credit: z.string().min(1), // 그림을 낸 곳 (원문 매체·회사·논문)
  url: z.url(), // 그림이 실린 원문 페이지
  width: z.number().int().positive().optional(),
  height: z.number().int().positive().optional(),
});

// 속보 카드: 한 소식을 설명하는 짧은 글. 큰 소식은 굵은 소제목 2~3개, 작은 소식은 문단 2~3개 (WRITING.md 3절).
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
    figure: figure.optional(),
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
    format: z.enum(['해설', '원문 요약', '정리', '갈리는 시각', '포트폴리오']), // 뒤 둘은 경제 섹션 (WRITING.md 6-5·6-6)
    summary: z.array(z.string()).length(3), // 3줄 요약
    sources: z.array(source).min(1),
    figure: figure.optional(),
  }),
});

export const collections = { cards, posts };
