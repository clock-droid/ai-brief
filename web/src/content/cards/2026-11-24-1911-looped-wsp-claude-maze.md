---
title: "클로드가 손으로 쓴 2만 개 가중치 트랜스포머, 미로 100% 풀어"
date: 2026-11-24T19:11:00+09:00
category: models
sources:
  - name: X (@ahmedmm72234641)
    url: https://x.com/ahmedmm72234641/status/2124869402634129901
  - name: MBZUAI — Looped Weight-Space Programming
    url: https://mbzuai-oryx.github.io/LoopedWSP/
    published: 2026-11-23T00:00:00+00:00
tweet:
  author: Ahmed Heakl
  handle: ahmedmm72234641
  text: "Today we introduce Looped Weight-Space Programming! 🚀 We asked Claude Opus 5.5 to solve hard mazes. It got only 26% right. Then we asked it to write a transformer that solves them, setting every weight directly. It took just 39 minutes and $19. No training. The model it… pic.twitter.com/gkZhuBcWv1"
  url: https://x.com/ahmedmm72234641/status/2124869402634129901
post: 2026-11-24-1911-looped-wsp-summary
---

- MBZUAI 연구진이 11월 23일 '루프형 가중치 공간 프로그래밍(Looped Weight-Space Programming)'을 공개함. 클로드 오퍼스 5.5가 학습 없이 트랜스포머의 가중치 하나하나를 직접 정해 써넣는 방식임.
- 30×30 미로(Maze-Hard)를 클로드가 글로 직접 풀면 26%만 맞혔지만, 클로드가 쓴 1만 9936개 가중치짜리 블록 하나를 1800번 반복 실행하자 시험 미로를 100% 풀었음. 100×100 미로도 풀었다고 함.
- 작성에 걸린 시간은 39분, 비용은 API 정가 기준 약 19달러. 180만~2700만 개 가중치로 학습한 기존 전용 모델(LDT 99.8%, TRM 91.9%, HRM 82.2%)보다 높음.
- 스도쿠 익스트림·하노이의 탑(원판 20개)·그래프 탐색 등 다른 과제에서도 쓴 트랜스포머가 100%를 기록함.
- 다만 동료 심사 전 연구 블로그이고, 저자들은 이미 알고리즘이 알려진 과제에만 맞는 방법이라고 밝힘.

한 줄 요약: 언어모델이 직접 풀지 못한 문제를, 그 문제를 푸는 작은 신경망의 가중치를 손으로 써서 풀어냄.

※ 언어처럼 정답 알고리즘이 없는 과제에 바로 적용되는 결과는 아님.
