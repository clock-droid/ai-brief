---
title: "OpenAI 내부 모델, 행렬 곱셈 지수 \"정확히 9/4\" 증명 공개"
date: 2026-11-25T11:11:00+09:00
category: science
sources:
  - name: OpenAI Math — The matrix multiplication exponent is nine fourths
    url: https://github.com/openai/math/blob/main/preprints/The-matrix-multiplication-exponent-is-nine-fourths-November-24-2026/README.md
    published: 2026-11-25T00:18:47+00:00
  - name: OpenAI Math — 공개 이력(history)
    url: https://github.com/openai/math/blob/main/history.md
    published: 2026-11-25T00:18:47+00:00
post: 2026-11-25-1111-ai-math-breakthroughs-month
---

- OpenAI가 이름을 밝히지 않은 내부 모델이 쓴 논문으로, 정사각 행렬 곱셈 지수(ω, n×n 행렬 곱에 드는 연산 수의 차수)가 모든 체(field)에서 정확히 9/4라고 11월 24일 공개함.
- 9/4 상한은 이미 나와 있었고(OpenAI 10월 결과 등), 이번 논문은 n≥2마다 곱셈·나눗셈 게이트가 최소 ⌈n^(9/4)/2⌉개 필요하다는 맞는 하한을 증명했다고 주장함.
- 오랜 추측 "ω = 2"는 성립하지 않는다는 뜻이고, 직사각 행렬 곱의 지수에도 새 제한(1/2 ≤ α ≤ 2/3)을 얻었다고 함.
- 나눗셈 없는 회로에서의 9/4 지수는 Lean(증명 검사 언어)으로 형식화돼 함께 공개됨.
- 다만 OpenAI 스스로 저장소 결과를 "가공 전 연구 데이터"라 부르며, 형식화 안 된 결과엔 오류가 있을 수 있다고 밝힘.

한 줄 요약: 행렬 곱셈의 최적 지수가 9/4로 확정됐다는 AI 작성 논문과 일부 Lean 증명이 나왔고, 학계 검토는 아직 시작 단계임.

※ 형식 산술 회로 모델에서의 결과로, 실제 컴퓨터의 실행 시간 하한을 그대로 뜻하지는 않음.
