---
title: "리만 Lean 압축판, 워털루서 검사기 6종 독립 재검사 통과"
date: 2026-11-28T09:11:00+09:00
category: science
post: 2026-11-25-1111-ai-math-breakthroughs-month
sources:
  - name: 워털루대 마이클 루빈스타인 — Alpöge/Claude proof of the Generalized Riemann Hypothesis (검증 기록)
    url: https://www.math.uwaterloo.ca/~mrubinst/alpoge_claude_grh/
    published: 2026-11-26T05:34:00+00:00
  - name: 루빈스타인 — The Alpöge–Claude proof of the Riemann hypothesis explained for the Riemann zeta function (초안)
    url: https://www.math.uwaterloo.ca/~mrubinst/alpoge_claude_grh/zeta-paper.pdf
    published: 2026-11-22T00:00:00+00:00
  - name: GitHub — lsernau/grh-lean (README, 배경)
    url: https://github.com/lsernau/grh-lean
  - name: GitHub — leanprover/comparator (README, 배경)
    url: https://github.com/leanprover/comparator
---

7만 6,000줄로 줄인 리만 가설 Lean 증명이 앤트로픽 바깥에서 다시 검사를 받았어요. 캐나다 워털루대 수학자 마이클 루빈스타인(Michael Rubinstein)이 11월 26일 압축판 794개 모듈을 모두 컴파일하고, 서로 다른 검사기 6종이 전부 받아들였다고 기록에 올렸어요. 다만 이건 "컴퓨터 검사를 남이 다시 돌려도 같은 결과가 나왔다"는 뜻이지, 수학자가 증명을 읽고 이해했다는 뜻은 아니에요.

**왜 다시 검사해?**

Lean은 증명을 코드로 적으면 컴퓨터가 한 단계씩 맞는지 확인해 주는 언어예요. 그런데 검사기 자체에 구멍이 있거나, 증명 코드가 몰래 추가 가정을 넣었거나, 증명한 정리가 원래 문제와 살짝 다르게 적혀 있으면 '통과'가 의미 없어져요. 그래서 같은 코드를 다른 사람이, 다른 검사기로 다시 돌리는 게 중요한데요. 원본(약 1,700만 줄)은 11월 21일 Lean·Mathlib 쪽 성명으로 확인됐지만, 25일 루크 서노(Luke Sernau)와 앤트로픽 동료들이 낸 압축판은 아직 바깥 검사가 없던 상태였어요.

**무엇이 확인됐어?**

루빈스타인 기록에 따르면 압축판의 다섯 정리는 Lean 기본 공리 세 개 말고는 다른 가정을 쓰지 않았고, 모든 모듈이 커널(증명을 최종 판정하는 Lean의 핵심 부분) 재생 검사를 통과했어요. 이어 '비교기(Comparator)'를 가장 엄격한 모드로 돌려, 증명된 다섯 문장이 미리 정해 둔 문제 파일과 정확히 같은지 확인했는데요. Lean 기본 커널과 엄격 모드 커널, 따로 만든 검사기인 나노다(nanoda)·lean4lean·con-leche·con-ron까지 6종이 모두 받아들였고, 약 5시간 뒤 "Your solution is okay!"가 떴다고 해요. 같은 기록은 MIT 앤드루 서덜랜드(Andrew Sutherland)도 원본과 압축판을 각각 검사했고, 격리 환경(샌드박스)에서 돌린 비교기도 같은 판정을 냈다고 정리했어요. 루빈스타인은 21일에도 원본 17만 5,187개 모듈을 워털루 서버에서 다시 검사했어요.

**어디까지 믿어도 돼?**

루빈스타인 쪽 압축판 검사는 계산 클러스터 사정으로 비교기의 샌드박스 없이 돌렸다고 스스로 밝혔어요. 또 그가 Claude·Codex·Gemini와 함께 쓰고 있는 265쪽짜리 사람용 해설 초안은 증명의 핵심 부등식 (M)을 13개 가정으로 쪼개 놓았을 뿐 아직 직접 증명하지 않은 '작업 중' 문서예요. 기계 검사의 신뢰도는 한 단계 올라갔고, 사람이 이해하는 증명은 여전히 진행 중인 셈이에요.
