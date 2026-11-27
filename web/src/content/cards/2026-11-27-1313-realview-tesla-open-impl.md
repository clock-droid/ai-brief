---
title: "머스크가 밝힌 테슬라 화면 구조, 맥북 1시간 46분 학습으로 재현"
date: 2026-11-27T13:13:00+09:00
category: robotics
sources:
  - name: GitHub — azet-llc/realview (README)
    url: https://github.com/azet-llc/realview
    published: 2026-11-27T00:00:00+00:00
  - name: "GeekNews — Show GN: RealView"
    url: https://news.hada.io/topic?id=37934
    published: 2026-11-27T02:49:37+00:00
  - name: arXiv — Mean Flows for One-step Generative Modeling (배경)
    url: https://arxiv.org/abs/2505.13447
figure:
  src: https://raw.githubusercontent.com/azet-llc/realview/main/assets/realview.gif
  alt: "세 칸 영상. 왼쪽은 실제 블랙박스 화면, 가운데는 RealView가 특징값만으로 그린 같은 도로, 오른쪽은 다른 야간 주행의 특징값을 넣어 그린 흐릿한 밤길"
  caption: "학습에 없던 주행에서 실제 화면(왼쪽)과 RealView 생성 화면(가운데), 다른 주행 특징값을 넣은 결과(오른쪽)"
  credit: azet-llc/realview
  url: https://github.com/azet-llc/realview
  width: 768
  height: 214
---

일론 머스크(Elon Musk)가 11월 22일 X에 짧게 설명한 테슬라 차량 화면 '리얼리티 뷰(Reality View)'의 구조를, 한 개발팀이 맥북 한 대로 학습해 코드와 가중치까지 공개했어요. 테슬라와 무관한 비공식 구현이에요.

머스크가 밝힌 구조는 이래요. 카메라 영상을 비전 인코더가 특징값으로 바꾸면, 별도의 확산 모델이 자기가 직전에 그린 화면에 노이즈를 섞었다가 걷어 내며 다음 8프레임을 그린다는 것. 즉 생성 모델은 카메라 영상을 직접 보지 않고 '차가 이해한 내용'만으로 화면을 다시 그려요. RealView는 이걸 고정된 DINOv2-small 인코더와 3,300만 파라미터 확산 트랜스포머로 옮겼어요. 한 번 계산으로 결과를 내는 '민 플로(mean flow)' 방식으로 학습해 8프레임을 한 번에 그리고, M4 맥스 맥북에서 1만 스텝 학습에 1시간 46분, 출력은 초당 86프레임이었다고.

학습에 없던 주행에서 그 주행의 특징값을 넣으면 생성 화면이 같은 순간을 63.8% 맞혔고, 다른 주행 특징값을 넣으면 1.5%로 무작위(2%)보다 낮았어요. 화면이 정말 인코더 정보에서 나온다는 확인인 것. 다만 야간 정확도는 26%에 그치고 먼 차량은 뭉개지며, 공개 데이터(comma2k19)로 만든 작은 재현이라 실제 테슬라 시스템과 같다는 뜻은 아니에요.
