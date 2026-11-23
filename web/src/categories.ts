// 분류 체계. 근거: Stanford AI Index 2026 장 구성 + HF Daily Papers 분야 분포 (research/02-leading-sources.md).
// collector/sources.json의 category, 글 frontmatter의 category가 모두 이 키를 쓴다.
export const CATEGORIES = {
  models: 'AI 모델·연구',
  agents: '에이전트·코딩',
  media: '생성 미디어',
  robotics: '로봇·자율주행',
  science: 'AI×과학',
  medicine: 'AI×의료',
  infra: '칩·컴퓨트',
  economy: '경제·산업',
  safety: '안전·정렬',
  policy: '정책·지정학',
  education: '교육',
  society: '여론·사회',
  tech: '테크',
  future: '에너지·우주',
  frontier: '장수·BCI·양자',
} as const;

export type CategoryKey = keyof typeof CATEGORIES;
export const CATEGORY_KEYS = Object.keys(CATEGORIES) as [CategoryKey, ...CategoryKey[]];
