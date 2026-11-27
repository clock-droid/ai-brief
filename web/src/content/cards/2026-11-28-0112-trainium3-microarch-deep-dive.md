---
title: "세미애널리시스 \"트레이니엄3, 같은 속도에서 이윤율 73.5%\""
date: 2026-11-28T01:12:00+09:00
category: infra
post: 2026-11-28-0112-semianalysis-trainium3-deep-dive-summary
sources:
  - name: "SemiAnalysis — AWS Challenger: Trainium3 Inference and Microarchitecture Deep Dive"
    url: https://newsletter.semianalysis.com/p/trainium3-inferencex
    published: 2026-11-27T15:54:59+00:00
figure:
  src: https://substack-post-media.s3.amazonaws.com/public/images/3be5b51d-209b-47b0-a776-0701b901dfa5_2048x1431.png
  alt: "가로축 사용자당 초당 토큰, 세로축 1달러당 토큰 수. 베라 루빈 곡선이 가장 위, 그 아래 트레이니엄3 곡선이 GB300·MI355X·TPU7x 곡선보다 위에 있는 그래프"
  caption: "GLM-5.2/5.3 에이전트 작업에서 응답 속도별 1달러당 토큰 수. 베라 루빈 다음으로 트레이니엄3가 높음"
  credit: SemiAnalysis
  url: https://newsletter.semianalysis.com/p/trainium3-inferencex
  width: 2048
  height: 1431
---

세미애널리시스(SemiAnalysis)가 11월 27일 아마존 AI 칩 트레이니엄3(Trainium3)를 뜯어본 장문 분석을 냈어요. 전날 '달러당 성능 GB300의 2.28배'라는 숫자의 근거를 칩 구조까지 내려가 설명한 글인데요. 같은 응답 속도(사용자당 초당 135토큰)에서 트레이니엄3+vLLM의 이윤율이 73.5%로, 2위 GB300+SGLang(53%)보다 높았다고 분석했어요.

왜 그런지는 일의 성격으로 갈려요. 답의 첫 글자가 나오기 전 질문 전체를 읽는 단계(프리필)는 계산량이 중요한데, 트레이니엄3의 FP4 연산 성능은 엔비디아 블랙웰 울트라의 17%뿐이라 첫 토큰까지 걸리는 시간은 아직 뒤진다고. 반면 한 글자씩 써 내려가는 단계(디코드)는 메모리에서 데이터를 꺼내는 속도가 중요한데, 메모리 대역폭은 GB300의 61%이면서 총소유비용(TCO)은 약 30%라 값 대비로는 앞선다는 거예요. 세미애널리시스는 이 장점이 아마존의 공급망만이 아니라, 데이터 이동 명령을 하드웨어가 만들어 주는 장치 같은 설계에서도 나온다고 봤어요.

다만 이윤율은 3년 임대 가격, Z.ai 정가, 가동률 60%라는 가정에서 계산한 거예요. 측정은 AWS 협조로 이뤄졌고, 랙 단위 연결 구조를 다룬 뒷부분은 유료라 확인하지 못했어요.
