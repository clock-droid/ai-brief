---
title: "MIT, 단백질 1억2,800만 개 학습한 생성 모델 'ProDiT' 공개"
date: 2026-11-28T17:12:00+09:00
category: medicine
sources:
  - name: Nature Machine Intelligence — Generating proteins with computationally predicted functions and multiple states via multimodal diffusion (Jing et al.)
    url: https://www.nature.com/articles/s42256-026-01329-2
    published: 2026-11-27T00:00:00+00:00
  - name: Nature Machine Intelligence — Generating proteins with complex functions (News & Views)
    url: https://www.nature.com/articles/s42256-026-01330-9
    published: 2026-11-27T00:00:00+00:00
---

MIT 컴퓨터과학·인공지능연구소(CSAIL) 보니 버거(Bonnie Berger) 연구팀이 원하는 기능을 지정하면 그에 맞는 새 단백질을 만들어 내는 AI 생성 모델 '프로디트(ProDiT)'를 11월 27일 네이처 머신 인텔리전스에 발표했어요. 다만 결과는 모두 컴퓨터 예측 단계이고, 실험실에서 만든 단백질로 확인한 건 아니에요.

예전 단백질 생성 모델은 대개 아미노산 서열이나 입체 구조 중 한쪽을 중심으로 다뤘는데요. 프로디트는 둘을 한 모델에서 함께 배우고, 거기에 '이 단백질이 무슨 일을 하는가'라는 기능 정보까지 붙였어요. 진화 전반에 걸친 단백질 1억 2,800만 개의 서열·구조·주석으로 학습했고, 유전자 온톨로지(Gene Ontology, 단백질 기능을 표준 용어로 분류한 목록) 기준 463가지 기능을 조건으로 줄 수 있다고 해요. 상황에 따라 켜졌다 꺼지는 것처럼 여러 상태를 오가는 단백질도 설계 목표로 삼을 수 있다는 점을 연구진은 기존 모델이 못 하던 부분으로 내세웠어요.

같은 호에 실린 해설(News & Views)에서 마이크로소프트 리서치의 사라 알람다리(Sarah Alamdari)·케빈 양(Kevin K. Yang)은 이 모델을 서열과 구조를 기능 맥락과 함께 배우는 "단순한" 생성 모델로 소개했어요. 원문은 유료라 초록 기준이고, 설계된 단백질이 실제로 그 기능을 하는지는 실험 검증이 남아 있어요.
