---
title: "독일 DLR, 제어 대신 '몸의 공진'으로 걷는 4족 로봇"
date: 2026-11-28T17:12:00+09:00
category: robotics
sources:
  - name: Nature Machine Intelligence — Exploring nonlinear body oscillations for natural quadruped gaits (Schmidt et al.)
    url: https://www.nature.com/articles/s42256-026-01320-x
    published: 2026-11-27T00:00:00+00:00
  - name: Wikipedia — Resonance (배경)
    url: https://en.wikipedia.org/wiki/Resonance
---

독일항공우주센터(DLR)와 뮌헨공대(TUM) 연구진이 로봇이 다리를 어떻게 움직일지 일일이 계산하는 대신, 몸이 원래 잘 흔들리는 방식(공진)을 찾아 그걸 걸음걸이로 바꾸는 방법을 11월 27일 네이처 머신 인텔리전스(Nature Machine Intelligence)에 발표했어요. 개념 증명(proof-of-concept) 단계지만, 걷는 능력을 제어 소프트웨어가 아니라 몸의 설계에서 끌어낸다는 방향이 새로워요.

**몸의 공진이 뭐야?**

그네를 탈 때 알맞은 박자에 맞춰 밀면 적은 힘으로도 크게 흔들리죠. 물체마다 이렇게 잘 흔들리는 고유한 방식이 있는데, 이게 공진(resonance)이에요. 연구진은 동물이 자세와 근육의 뻣뻣함을 조절해 이런 공진을 이용하기 때문에, 속도마다 힘을 덜 들이는 걸음걸이를 쓴다고 설명해요. 반면 대부분의 4족 로봇은 몸이 복잡하게(비선형으로) 흔들려 예측하기 어렵다 보니 공진을 쓰도록 설계되지 않았고, 걸음을 만드는 전용 제어기가 따로 필요했어요.

**이번엔 뭘 보였어?**

연구진은 몸이 아주 유연한 4족 로봇 '이버트(eBert)'에서 새 이론 도구로 비선형 정규 모드(nonlinear normal modes, 비선형 시스템이 스스로 반복하는 진동 패턴) 6개를 찾아냈고, 시뮬레이션과 실제 로봇에서 그 모드가 실제로 있음을 확인했어요. 보폭만 블랙박스 최적화로 정해 주자 시뮬레이션에서 모드마다 서로 다른 걸음걸이가 자연스럽게 나왔고 속도도 각각 달랐다고 해요. 중력·관성·탄성이 걸음을 만들어 낸 셈인 것.

다만 시뮬레이션 결과가 실제 로봇에는 "대부분" 옮겨졌다는 정도이고, 연구진도 이를 개념 증명이라고 불렀어요. 원문은 유료라 초록 기준이에요.
