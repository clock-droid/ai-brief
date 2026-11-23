---
title: "3차원 오일러 방정식, 매끄러운 초기값에서 유한 시간 특이점 증명"
date: 2026-11-24T07:09:00+09:00
category: science
sources:
  - name: Terence Tao 블로그 (Matei Coiculescu 게스트 글)
    url: https://terrytao.wordpress.com/2026/11/23/finite-time-singularity-formation-for-the-three-dimensional-euler-equations/
    published: 2026-11-23T20:39:56+00:00
---

- 알푀게(Levent Alpöge), 벅마스터(Tristan Buckmaster), 코이쿨레스쿠(Matei Coiculescu)가 3차원 비압축성 오일러 방정식(마찰 없는 이상 유체의 운동 방정식)에서 유한 시간 특이점(해가 유한한 시간 안에 매끄러움을 잃는 현상)이 생김을 증명했다는 논문(arXiv:2611.26772)을 냈음.
- 주기 경계(3차원 토러스)에서 매끄러운 초기 속도장으로 출발해도 속도 자체는 유한하게 유지된 채 속도 기울기와 소용돌이도(vorticity)가 원점에서 발산함.
- 파동 섭동을 여러 규모로 겹쳐 쌓는 반복 구성을 쓰고, 초기값은 경계값 문제를 풀어 정함.
- 11월 23일 코이쿨레스쿠가 테런스 타오(Terence Tao) 블로그에 증명의 구성 요소를 설명하는 게스트 글을 올림.
- 다만 이 글은 증명 전체가 아닌 개요이며, 검증은 논문 본문 확인이 필요함.

한 줄 요약: 3차원 오일러 방정식에서 특이점이 생기는 매끄러운 초기값이 존재한다는 증명이 공개됨.

※ 점성이 없는 오일러 방정식에 대한 결과이며, 밀레니엄 난제인 나비에-스토크스 방정식을 푼 것은 아님.
