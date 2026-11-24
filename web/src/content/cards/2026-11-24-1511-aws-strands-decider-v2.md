---
title: "AWS, 고르기 전용 오픈 모델 Strands Decider v2 5종 공개"
date: 2026-11-24T15:11:00+09:00
category: models
sources:
  - name: Strands Agents 블로그
    url: https://strandsagents.com/blog/introducing-strands-decider-v2/
    published: 2026-11-23T00:00:00+00:00
  - name: Techmeme (The New Stack)
    url: https://www.techmeme.com/261123/p55#a261123p55
    published: 2026-11-24T04:25:01+00:00
---

- AWS의 Strands Labs가 11월 23일 '결정 모델(decision model)' Strands Decider v2를 공개함. 구글 젬마 4(Gemma 4) 기반 E2B·E4B·12B·26B-A4B·31B 5종이며 Apache 2.0 라이선스로 허깅페이스에 가중치를 올림.
- 글을 생성하지 않고, 개발자가 준 선택지마다 확률을 한 번의 연산(forward pass)으로 매김. 도구 선택, 모델 라우팅, 답변 품질 판정 같은 용도임.
- 공개 텍스트 벤치마크 6개 평균은 31B가 82.1점으로, v1 26B-A4B(70.0점)보다 12.1점 높음. 보정 오차(ECE)는 0.062에서 0.027로 줄어듦.
- 학습 데이터는 v1의 13만 6천 건에서 1,748만 건으로 늘었음.
- 다만 성능 수치는 AWS 자체 발표이고, v2 31B를 더 작은 v1 모델과 비교한 것임.

한 줄 요약: AWS가 에이전트의 '고르기' 판단만 맡는 오픈 모델을 5가지 크기로 새로 냄.
