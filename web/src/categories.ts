// 분류 체계. 사이트는 두 섹션(AI, 경제)으로 나뉘고, 분류마다 한 섹션에 속한다.
// collector/sources.json의 category, 글 frontmatter의 category가 모두 이 키를 쓴다.

// AI 섹션. 근거: Stanford AI Index 2026 장 구성 + HF Daily Papers 분야 분포 (research/02-leading-sources.md).
// 교육·대학과 창업은 AI가 바꾸는 배움·일하는 방식의 변화를 다룬다 (2026-11-28 사용자 결정). 창업 회사의 투자·가치는 경제 분류.
export const AI_CATEGORIES = {
  models: 'AI 모델·연구',
  agents: '에이전트·코딩',
  media: '생성 미디어',
  robotics: '로봇·자율주행',
  science: 'AI×과학',
  medicine: 'AI×의료',
  infra: '칩·컴퓨트',
  safety: '안전·정렬',
  policy: '정책·지정학',
  education: '교육·대학',
  startups: '창업',
  society: '여론·사회',
  tech: '테크',
  future: '에너지·우주',
  frontier: '장수·BCI·양자',
} as const;

// 경제 섹션 (2026-11-28 사용자 결정: 메뉴에 경제를 따로, 분류는 잘게). AI 기업의 상장·투자·실적도 여기로 온다.
export const ECON_CATEGORIES = {
  rates: '금리·중앙은행',
  markets: '주식시장',
  companies: '기업·실적',
  commodities: '에너지·원자재',
  trade: '무역·지정학',
  investors: '투자자',
} as const;

export const CATEGORIES = { ...AI_CATEGORIES, ...ECON_CATEGORIES } as const;

export type CategoryKey = keyof typeof CATEGORIES;
export const CATEGORY_KEYS = Object.keys(CATEGORIES) as [CategoryKey, ...CategoryKey[]];

export const SECTIONS = {
  ai: { label: 'AI', feed: '/', posts: '/posts/', categories: Object.keys(AI_CATEGORIES) as CategoryKey[] },
  econ: { label: '경제', feed: '/econ/', posts: '/econ/posts/', categories: Object.keys(ECON_CATEGORIES) as CategoryKey[] },
} as const;

export type SectionKey = keyof typeof SECTIONS;
export const SECTION_KEYS = Object.keys(SECTIONS) as SectionKey[];

export const sectionOf = (category: CategoryKey): SectionKey => (category in ECON_CATEGORIES ? 'econ' : 'ai');
