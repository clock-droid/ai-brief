---
title: "쇼어 알고리즘 최적화, AI가 내면 Lean이 검증"
date: 2026-11-26T11:13:00+09:00
category: science
sources:
  - name: Quantum Computing Report — Zapata Quantum and University of Maryland Launch ForShor.ai
    url: https://quantumcomputingreport.com/zapata-quantum-and-university-of-maryland-launch-forshor-ai-formal-verification-challenge-for-ai-assisted-quantum-algorithm-design/
    published: 2026-11-26T02:05:25+00:00
---

양자컴퓨터로 소인수분해를 하는 쇼어(Shor) 알고리즘의 핵심 계산을 더 싸게 만드는 방법을, 사람과 AI 에이전트가 내고 컴퓨터가 수학적으로 검증하는 공개 대회가 열렸어요. 자파타 퀀텀(Zapata Quantum)과 메릴랜드대가 만든 ForShor.ai로, 쇼어 본인이 과학 자문을 맡았어요.

방식은 이래요. 참가자는 큰 수 곱셈을 어떻게 쪼개고 덧셈·시프트를 어떤 순서로 할지 정하는 '계획표'만 제출해요. 그러면 Lean 4(증명을 코드로 쓰면 컴퓨터가 한 단계씩 맞는지 검사하는 언어)로 짠 검증기가 네 가지 조건을 확인하고, 통과하면 그 계획이 쇼어 알고리즘의 성공 확률과 계산량 증가 속도(O(n^(2+ε)))를 지킨다는 증명을 자동으로 물려받아요. 검증기는 Lean 파일 약 180개, 선언 약 3,500개 규모예요. 2048비트 기준으로 가능한 계획을 전부 따져 보려면 약 3.2×10^51 코어시간이 든다고 해 AI 탐색에 맡기자는 것.

AI가 찾은 회로 개선은 그동안 왜 맞는지 들여다보기 어려운 '블랙박스'라는 지적을 받았는데요. 주최 측은 검증을 통과한 결과만 순위표에 올려 다른 양자 소프트웨어에서도 다시 쓸 수 있게 하겠다고 했어요. 대회는 6주간 열리고, 자파타 자체 소프트웨어 플랫폼의 시험대 역할도 겸해요.
