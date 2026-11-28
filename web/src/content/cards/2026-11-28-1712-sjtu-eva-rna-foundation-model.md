---
title: "RNA 1억1,400만 개 학습한 'EVA', 9개 벤치 중 7개 1위"
date: 2026-11-28T17:12:00+09:00
category: medicine
sources:
  - name: Nature Machine Intelligence — A long-context generative foundation model for versatile RNA design (Huang, Lv, Gao et al.)
    url: https://www.nature.com/articles/s42256-026-01321-w
    published: 2026-11-27T00:00:00+00:00
---

상하이교통대·칭화대 등 중국 연구진이 RNA를 설계하는 AI 기반 모델 'EVA(Evolutionary Versatile Architect)'를 11월 27일 네이처 머신 인텔리전스에 발표했어요. 기존 RNA 생성 모델이 짧은 조각만 다루던 한계를 넘어, 전사체 전체 길이의 RNA를 한 모델로 다룬다는 게 핵심이에요.

RNA는 유전 정보를 옮기거나 그 자체로 일을 하는 분자인데요, mRNA 백신이나 유전자 편집 도구 크리스퍼(CRISPR)의 안내 RNA도 여기에 속해요. 연구진은 기존 모델이 문맥 창(한 번에 볼 수 있는 길이)이 짧아 RNA 전체 구조를 배우기 어려웠다고 보고, 진화 전반에서 모은 RNA 1억 1,400만 개 이상을 8,192토큰 길이로 학습시켰어요. 전문가 혼합(MoE, 입력마다 일부 하위 모델만 쓰는 구조) 방식을 썼고, 변이가 기능에 주는 영향 예측부터 여러 종류의 RNA 설계까지 한 모델로 처리한다고 해요.

결과는 세 갈래예요. 기존 평가 9개 중 7개에서 최고 성능을 냈고, 자연 RNA 구조 특징 분포와의 차이는 이전 오픈소스 RNA 생성 모델보다 10배 넘게 작았다고 해요. 실험실 검증도 일부 했는데, 표적에 달라붙는 RNA(앱타머)는 대조군보다 형광 세기와 결합력이 각각 약 2배 좋아졌다고. 다만 실험 검증은 시험관 수준이고, 치료용 mRNA 등 다른 설계는 주로 컴퓨터 평가예요. 원문은 유료라 초록 기준이에요.
