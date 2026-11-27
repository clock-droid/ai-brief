---
title: "세미애널리시스: 베라 루빈, GB300보다 달러당 토큰 2~6.5배"
date: 2026-11-27T19:12:00+09:00
category: infra
sources:
  - name: X (@SemiAnalysis_)
    url: https://x.com/SemiAnalysis_/status/2126235662009389501
    published: 2026-11-27T08:44:20+00:00
  - name: SemiAnalysis — AgentX - InferenceXv3 (배경)
    url: https://newsletter.semianalysis.com/p/agentx-inferencexv3-does-cuda-moat
    published: 2026-08-24T00:00:00+00:00
  - name: NVIDIA 기술 블로그 — AgentX 벤치마크 설명 (배경)
    url: https://developer.nvidia.com/blog/nvidia-vera-rubin-and-blackwell-set-a-new-standard-for-agentic-ai-performance-per-watt/
tweet:
  author: SemiAnalysis
  handle: SemiAnalysis_
  text: "Rubin’s lead grows with interactivity. Same TokenSpeed engine on both racks: Vera Rubin NVL72 gets 2-6.5x GB300 NVL72's tokens per $ TCO https://t.co/GstKolvdSh"
  url: https://x.com/SemiAnalysis_/status/2126235662009389501
post: 2026-11-27-1912-agentx-benchmark-explainer
---

반도체 분석 회사 세미애널리시스(SemiAnalysis)가 엔비디아 차세대 랙 '베라 루빈 NVL72(Vera Rubin NVL72)'가 현행 GB300 NVL72보다 같은 돈으로 2~6.5배 많은 토큰을 뽑아냈다고 11월 27일 X에 밝혔어요. 응답을 빠르게 내야 하는 조건일수록 차이가 커졌다는 게 핵심이에요.

**무엇을 비교했어?**

함께 올린 그래프는 큐원3.8 플래시 넥스트 176B(Qwen3.8 Flash Next 176B) 모델로 에이전트 작업을 돌렸을 때, 총소유비용(TCO) 1달러당 처리한 토큰 수를 비교한 거예요. 총소유비용은 칩 값만이 아니라 서버를 소유·운영하는 데 드는 비용을 합친 개념이에요. 두 랙 모두 FP4 정밀도에 같은 추론 엔진(TokenSpeed)을 썼다고 해서, 소프트웨어 차이가 아니라 하드웨어 차이를 본 셈이에요.

**왜 '2배'와 '6.5배'가 같이 나와?**

가로축이 사용자 한 명이 받는 토큰 속도(P90 인터랙티비티, 초당 토큰)인데요. 서버는 여러 요청을 한꺼번에 묶어 처리할수록 싸지지만, 그만큼 한 사람에게 돌아가는 속도는 느려져요. 그래프에서 사용자당 초당 약 215토큰 지점에선 차이가 2.20배였고, GB300이 낼 수 있는 가장 빠른 구간(약 365토큰)에선 6.51배로 벌어졌어요. GB300은 빠른 응답을 요구받으면 효율이 급히 떨어지고, 루빈은 그보다 훨씬 빠른 구간(600토큰 이상)까지 곡선이 이어지는 것.

하루 전 세미애널리시스는 아마존 트레이니엄3 서버가 같은 계열 벤치마크에서 GB300보다 달러당 성능 2.28배라고 발표했어요. 이번 결과는 엔비디아 쪽 차세대 제품의 답인 셈인데요. 다만 트레이니엄3 결과와 모델·조건이 같은지는 확인되지 않아 두 숫자를 바로 비교할 수는 없어요.

**어디까지 믿어도 돼?**

8월 엔비디아는 자체 측정으로 루빈이 GB300보다 메가와트당 처리량이 최대 30배라고 했지만, 당시엔 "세미애널리시스 검토 대기 중"이라고 밝혔어요. 이번 숫자는 세미애널리시스가 낸 그래프지만, 가격(TCO)을 어떤 가정으로 잡았는지는 이 카드에서 확인하지 못했어요. 한 모델·한 작업 기준의 결과라는 점도 감안해야 해요.
