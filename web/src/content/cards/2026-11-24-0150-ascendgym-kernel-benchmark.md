---
title: "화웨이 Ascend 커널 최적화 벤치 AscendGYM, 1위 Opus 5"
date: 2026-11-24T01:47:00+09:00
category: infra
sources:
  - name: arXiv 2611.17621
    url: https://arxiv.org/abs/2611.17621
    published: 2026-11-13T00:00:00+00:00
  - name: Import AI 482
    url: https://importai.substack.com/p/import-ai-482-huawei-kernel-benchmarks
    published: 2026-11-23T00:00:00+00:00
---

- 선전 SLAI 연구팀이 11월 13일 AscendGYM을 arXiv에 공개함(20일 v2). AI 에이전트가 화웨이 Ascend NPU용 기존 커널(GPU·NPU에서 도는 연산 코드)을 얼마나 빠르게 고치는지 재는 벤치마크임.
- 커널 48개를 세 난이도로 나눴고, 실제 학습·추론 작업의 자료형과 텐서 크기를 시험 케이스로 씀.
- 속도 향상을 토큰 비용과 함께 따지는 지표 STS(Speedup-Token Score)를 제안함.
- Import AI 482에 따르면 순위는 Opus 5, GPT-5.6, GLM-5.3 순이고 Claude Code가 절대 점수가 가장 높았음. GPT-5.6이 토큰 효율이 가장 좋았음.
- 다만 abstract에는 수치와 순위가 없고, 순위는 Import AI 소개 기준이며 원 점수는 확인하지 못함.

한 줄 요약: 엔비디아가 아닌 중국산 칩용 커널을 AI가 얼마나 짜는지 재는 공개 벤치마크가 나옴.
