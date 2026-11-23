---
title: "구글, 트랜스포머 잔차연결 대체 DCA…같은 품질 최대 3배 빨리"
date: 2026-11-24T02:30:00+09:00
category: models
sources:
  - name: Google Research
    url: https://research.google/blog/supercharging-transformer-residual-connections/
    published: 2026-11-23T00:00:00+00:00
---

- 구글 리서치(Google Research)가 11월 23일 블로그에 딥크로스어텐션(DeepCrossAttention, DCA)을 소개함. ICML 2025 논문의 구조임.
- 기존 잔차연결(residual connection, 층의 입력을 출력에 그대로 더하는 지름길)은 이전 층 정보를 같은 비중으로 더해서, 층이 깊어질수록 초기 층의 세부 정보가 희석됨.
- DCA는 토큰마다 이전 층들의 출력을 얼마나 섞을지 가중치를 학습하고, 층 방향으로 교차 어텐션(depth-wise cross-attention)을 적용함.
- C4·LM1B 언어모델링 실험에서 표준 트랜스포머와 같은 성능에 최대 5배 적은 학습 스텝으로 도달함. 퍼플렉시티 14 미만을 내는 데 표준 모델은 42층, DCA는 30층이면 됨(29% 감소).
- 다만 블로그가 제시한 결과는 LM1B·C4 규모의 실험이며, 최신 대형 모델에서의 효과는 밝히지 않음.

한 줄 요약: 층 사이 연결을 학습으로 고르는 구조로, 같은 품질을 더 적은 학습·층 수로 내는 결과를 구글이 소개함.
