---
title: "구글, 코딩 에이전트를 리서처로…'딥 리서치' 스킬 공개"
date: 2026-11-28T01:12:00+09:00
category: agents
tweet:
  author: Philipp Schmid
  handle: _philschmid
  text: "We built an experimental deep research skill for Gemini 4 Neon, turning coding agents into researchers 🚀\n\nWhat the skill focuses on:\n1. Scope: simple direct, broad ones in 3-5 angles\n2. Subagents: parallel search or browser, 8-12 step cap\n3. Sources: primary filings and PDFs, no https://t.co/Bn6GSZd8iO"
  url: https://x.com/_philschmid/status/2126312943520243885
sources:
  - name: X (@_philschmid)
    url: https://x.com/_philschmid/status/2126312943520243885
  - name: GitHub — google-gemini/demolab
    url: https://github.com/google-gemini/demolab
  - name: GitHub — deep-research SKILL.md
    url: https://github.com/google-gemini/demolab/blob/main/skills/deep-research/SKILL.md
---

구글 딥마인드(Google DeepMind)의 필립 슈미트(Philipp Schmid)가 11월 27일, 제미나이 4 네온(Gemini 4 Neon)용 실험적 '딥 리서치(deep research)' 스킬을 공개했어요. 코딩 에이전트를 조사원으로 바꾸는 지침 파일이라고. 스킬은 에이전트가 특정 일을 할 때 꺼내 읽는 작업 설명서 같은 거예요.

스킬 파일을 보면 질문을 먼저 가르는데요. 사실 하나를 묻는 질문엔 바로 답하거나 하위 에이전트를 2개까지만 쓰고, 넓은 주제는 겹치지 않는 3~5개 하위 질문으로 나눠 하위 에이전트들이 동시에 찾게 해요. 각자 검색·도구 사용은 8~12단계로 묶고, 다 쓰면 그때까지 확인한 것과 빈 곳을 돌려준다고. 주장은 검색 결과 요약이 아니라 원 자료로 확인하고, 핵심 숫자는 정확한 인용을 붙이게 했어요. 보고서는 두 문장 요약으로 시작해 출처 링크를 달고, 자료가 엇갈리면 '해결 안 된 점'을 따로 적어요.

저장소는 제미나이 4 모델로 블라인드 평가 수백 번을 거쳤고 평가자가 90% 넘게 이 스킬의 결과를 골랐다고 적었어요. 다만 무엇과 비교했는지와 평가 방식은 공개하지 않은 자체 측정이에요. 안티그래비티와 클로드 코드에도 설치할 수 있다고 해요.
