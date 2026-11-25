---
title: "METR \"오픈AI 사전학습 손실, 7배 빨리 떨어져\""
date: 2026-11-25T09:11:00+09:00
category: models
post: 2026-11-25-0911-metr-pretraining-loss-summary
sources:
  - name: METR
    url: https://metr.org/blog/2026-11-24-interpreting-a-recent-acceleration-in-pretraining-loss/
    published: 2026-11-24T08:00:00+00:00
figure:
  src: https://metr.org/assets/images/pretraining-loss-acceleration/logloss_hinge.png
  alt: "GPT-3.5부터 GPT-6.2 Astra까지 오픈AI 모델의 로그 퍼플렉시티를 출시일 순으로 찍고, 2026년 2월을 꺾이는 점으로 두 직선을 맞춘 그래프"
  caption: "오픈AI 모델별 로그 퍼플렉시티. 2026년 2월 이후 기울기가 이전보다 7.1배 가파름"
  credit: METR (OpenAI 자료)
  url: https://metr.org/blog/2026-11-24-interpreting-a-recent-acceleration-in-pretraining-loss/
  width: 1880
  height: 1211
---

- AI 평가 기관 METR가 오픈AI가 공개한 13개 모델의 사전학습 손실 자료를 분석한 글을 11월 24일 냄.
- 자체 코드베이스 데이터로 잰 로그 퍼플렉시티(다음 토큰을 얼마나 틀리게 예측하는지의 평균)가 2026년 2월 이후 연 0.156씩 떨어져, 2022~2025년(연 0.022)보다 약 7배 빨라졌다고 함.
- 이 속도면 GPT-3.5→GPT-4.1에 3년 걸린 하락폭을 약 6개월 반에 따라잡음.
- 다만 같은 기간 오픈AI 모델의 벤치마크 점수는 비슷하게 빨라지지 않았고, 이를 어떻게 해석할지 METR 안에서도 합의가 없다고 밝힘.

한 줄 요약: 사전학습 손실은 크게 빨라졌지만, 그것이 실제 능력 가속으로 이어질지는 METR도 판단을 유보함.
