---
title: "셸벤치: 최고 AI 에이전트도 실무 과제 62.5%만 완수"
date: 2026-11-24T23:13:00+09:00
category: agents
sources:
  - name: OpenClaw 블로그
    url: https://openclaw.ai/blog/shellbench
    published: 2026-11-24
  - name: X (@vincent_koc)
    url: https://x.com/vincent_koc/status/2125209543894614117
    published: 2026-11-24T12:46:54+00:00
  - name: Techmeme (The Deep View)
    url: https://www.techmeme.com/261124/p18#a261124p18
    published: 2026-11-24T13:25:01+00:00
tweet:
  author: Vincent Koc
  handle: vincent_koc
  text: "Secret is out, we are releasing a benchmark for claws after months of hard work from a huge team of researchers and engineers across industry helping to make this happen https://t.co/bbO2sv1EPc"
  url: https://x.com/vincent_koc/status/2125209543894614117
post: 2026-11-24-2313-shellbench-summary
figure:
  src: https://openclaw.ai/blog/shellbench/model-harness-pass-rates-dark-v3.png
  alt: "모델 12개와 하네스 5개(OpenClaw, Pi, Hermes, Codex, Claude Code)별 1회 시도 통과율 표. GPT-6 Astra 62.5, Claude Fable 5.2 61.9, GPT-6.1 Sol 61.4가 상위이고 GPT-6 Luna 18.8이 최하위"
  caption: "모델·하네스별 1회 시도 통과율. 상위 3개 모델이 1.1점 안에 몰려 있고, 하네스 평균 차이는 2.36점에 그침"
  credit: OpenClaw
  url: https://openclaw.ai/blog/shellbench
  width: 1400
  height: 895
---

- 오픈클로 재단(OpenClaw Foundation)이 11월 24일 영수증 정리·최신 정보 확인·수상한 결제 요청 걸러내기 같은 일상 업무형 에이전트 벤치마크 '셸벤치(ShellBench)'를 공개함. 허깅페이스·레드햇·UC 버클리 등이 함께 만듦.
- 모델 12개 × 하네스(에이전트 실행 틀) 5개로 과제 100개를 돌려 5만 3,100회를 채점함.
- 1위 GPT-6 Astra도 평균 통과율 62.5%에 그쳤고, Claude Fable 5.2(61.9%)·GPT-6.1 Sol(61.4%)이 뒤를 이음.
- 모델을 바꾸면 점수가 중앙값 45.7점 차이 났지만, 하네스를 바꾸면 6.2점 차이에 그침.
- 다만 전체 논문은 아직 공개 전이고, 재단이 직접 만든 벤치마크임.

한 줄 요약: 최상위 모델도 실무형 에이전트 과제 10개 중 4개 가까이를 끝내지 못함.

※ 정답 기준을 하나라도 어기면 실패로 치는 엄격한 채점 방식의 결과임.
