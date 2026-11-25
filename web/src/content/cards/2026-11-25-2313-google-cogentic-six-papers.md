---
title: "구글 AI 에이전트, 수학 논문 6편 하루에 공개…소인수분해 L[1/3] 증명 주장"
date: 2026-11-25T23:13:00+09:00
category: science
sources:
  - name: Google Research GitHub — Cogentic Research Papers
    url: https://github.com/google-research/google-research/tree/master/cogentic_research_papers
    published: 2026-11-25T00:00:00+00:00
  - name: Unconditional Integer Factorization in Time L_N[1/3, O(1)] (논문 PDF)
    url: https://github.com/google-research/google-research/blob/master/cogentic_research_papers/integer_factorization/paper.pdf
    published: 2026-11-25T00:00:00+00:00
  - name: arXiv — Cogentic (2609.40324)
    url: https://arxiv.org/abs/2609.40324
  - name: OfficeChai — Google's Cogentic AI Releases Six Math Papers In One Day
    url: https://officechai.com/ai/googles-cogentic-ai-releases-six-math-papers-in-one-day-including-a-proven-fast-algorithm-for-factoring-numbers/
    published: 2026-11-25T00:00:00+00:00
post: 2026-11-25-2313-cogentic-factoring-explainer
---

구글 리서치(Google Research)가 11월 25일, 자사 AI 수학 에이전트 '코젠틱(Cogentic)'이 쓴 논문 6편을 깃허브에 한꺼번에 올렸어요. 가장 눈에 띄는 건 소인수분해를 '증명된' 속도로 L[1/3] 수준까지 끌어내렸다는 논문인데요. 다만 아직 동료 심사를 거치지 않은 주장이에요.

**코젠틱이 뭐야?**

구글 리서치·딥마인드 연구진이 9월 arXiv에 공개한 에이전트 틀(framework)이에요. 증명을 시도하는 에이전트, 반박을 찾는 검증 에이전트, 문헌을 찾는 에이전트, 논문을 쓰는 에이전트가 역할을 나눠 일하는 구조예요. 논문마다 붙은 설명에 따르면 이번 논문들과 Lean 4(컴퓨터가 증명을 검사하는 언어) 형식화는 모두 제미나이 4(Gemini 4)를 바탕 모델로 "전적으로 코젠틱이 얻은 것"이고, 처음에 증명과 형식화를 요청한 것 말고는 사람의 개입이 없었다고 해요.

**이번엔 뭐가 달라졌어?**

큰 수를 소수로 쪼개는 소인수분해는 RSA 암호의 안전성과 맞닿은 문제예요. 실제로 가장 빠른 방법인 일반 수체 체(GNFS)는 L[1/3]이라는 속도 등급으로 돌아가지만, 그 속도는 증명되지 않은 가정에 기대고 있었는데요. 가정 없이 증명된 최고 기록은 1992년 렌스트라(Lenstra)·포머런스(Pomerance)의 L[1/2]였어요. 코젠틱 논문은 가정 없이 L[1/3]을 증명했다고 주장해요. 34년 묵은 '실전 속도'와 '증명된 속도' 사이의 틈을 메웠다는 것.

나머지 5편은 결정론적 소인수분해, 이산로그, 2인 게임의 내시 균형 근사, 로그-랭크 추측, 하라리(Harary)의 간선 재구성 추측을 다뤄요. 같은 저장소에는 11월 18일·23일 날짜로 코젠틱 논문 3편이 먼저 올라 있었어요.

**어디까지 믿어도 돼?**

L[1/3] 논문의 상수는 105로, GNFS의 약 1.9보다 훨씬 커요. 실제 암호를 더 빨리 깨는 방법이 아니라 이론상 결과인 것. 로그-랭크 논문의 개선 폭도 지수에서 0.000005예요. Lean 형식화는 완성됐다고 했지만 아직 공개하지 않았고 "후속 제출"로 내놓겠다고 했어요. 저장소에는 "구글 공식 제품이 아니다"라는 문구도 붙어 있어요.
