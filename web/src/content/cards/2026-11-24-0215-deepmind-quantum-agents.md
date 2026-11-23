---
title: "DeepMind, Gemini 4 에이전트로 양자 회로 비용 최대 10배 절감"
date: 2026-11-24T02:08:00+09:00
category: science
sources:
  - name: Google DeepMind
    url: https://deepmind.google/blog/finding-faster-quantum-algorithms-with-agents-and-formal-verification/
    published: 2026-11-23T16:59:40+00:00
  - name: arXiv 2611.09822
    url: https://arxiv.org/abs/2611.09822
tweet:
  author: Google DeepMind
  handle: GoogleDeepMind
  text: "Quantum computers could one day transform fusion energy, chemistry, and drug discovery - if we can make the algorithms efficient enough to run on early hardware. Using teams of Gemini 4 agents, we’ve built new quantum circuits that cut future simulation costs by up to 10 times. pic.twitter.com/H6xArBtsvQ"
  url: https://x.com/GoogleDeepMind/status/2124911073266413634
---

- 구글 딥마인드(Google DeepMind)가 구글 퀀텀 AI(Google Quantum AI)와 함께 Gemini 4 에이전트 팀으로 기존 양자 알고리즘을 개선했다고 11월 23일 공개함.
- 문제마다 독립된 에이전트 팀을 두고, 결과는 Lean(증명을 기계로 검사하는 언어)으로 맞다고 증명된 뒤에야 공유 노트에 올렸음. 팀들은 4시간마다 가상 "학회"를 열어 아이디어를 교환함.
- 핵심융합(관성 가둠 방식) 시뮬레이션의 연산 비용은 11.8배 줄고, 필요한 오류 정정 큐비트는 5,650개에서 4,338개로 감소함.
- 광반응 분자 시뮬레이션은 8배, 약물 대사 효소 시토크롬 P450은 2.5배 저렴해졌고 큐비트는 481개에서 333개로 줄음. 그로버 알고리즘 구현은 2.57배, 아크사인 루틴은 290배 빨라짐.
- Lean 라이브러리, 문제 명세, 검증된 해법은 GitHub에 공개함.
- 다만 개선된 알고리즘도 첫 오류 정정 양자컴퓨터가 제공할 자원보다 더 많은 자원이 필요하다고 글에서 밝힘.

한 줄 요약: AI 에이전트가 증명 검증을 거친 양자 회로 개선안을 내놨고, 실제 하드웨어에서 돌리려면 아직 자원이 더 필요함.
