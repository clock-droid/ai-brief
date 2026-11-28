---
title: "번스타인, 증명 검사기 '건전성 버그' 목록 공개…Lean 23건"
date: 2026-11-28T15:15:00+09:00
category: science
post: 2026-11-25-1111-ai-math-breakthroughs-month
sources:
  - name: cr.yp.to — False computer-checked proofs (D. J. Bernstein)
    url: https://cr.yp.to/proofs/falseccp.html
    published: 2026-11-27T22:33:58+00:00
  - name: GeekNews — 컴퓨터 검증을 통과한 거짓 증명
    url: https://news.hada.io/topic?id=37975
    published: 2026-11-27T23:43:25+00:00
  - name: 워털루대 마이클 루빈스타인 — Alpöge/Claude proof of the Generalized Riemann Hypothesis (배경)
    url: https://www.math.uwaterloo.ca/~mrubinst/alpoge_claude_grh/
    published: 2026-11-26T05:34:00+00:00
---

'컴퓨터가 검사한 증명은 틀릴 수 없다'는 믿음에 암호학자 대니얼 J. 번스타인(Daniel J. Bernstein)이 숫자로 반론을 냈어요. 그는 자기 사이트에 주요 증명 검사기 7종에서 보고된 '건전성 버그(soundness bug)' 목록을 정리해 11월 25일 판으로 올렸고, 28일 국내 개발자 커뮤니티에도 소개됐는데요. Lean 3·4에서만 23건이 모였어요.

**건전성 버그가 뭐야?**

증명 검사기는 증명의 모든 단계를 규칙대로 따져 '맞다'고 도장을 찍는 프로그램이에요. 건전성 버그는 이 도장이 거짓 명제에도 찍히게 만드는 결함이에요. 시험 채점기가 특정 답안에선 틀린 답에도 동그라미를 치는 셈인데요. 번스타인은 이런 버그 상당수가 실제로 거짓 증명을 통과시키는 데 악용될 수 있음이 이미 입증됐다고 썼어요.

목록에 따르면 보고 건수는 HOL Light 3건, 미자르(Mizar) 7건, 메타매스(Metamath) 9건, 이자벨(Isabelle) 20건, Lean 23건, HOL4 24건, 콕(Coq·지금 이름은 Rocq) 111건이에요. Lean 23건 가운데 10건이 올해 보고된 것이에요.

**리만 증명과는 무슨 상관이야?**

이번 리만 가설 증명은 1,700만 줄 Lean 코드로 나왔고, 그 신뢰는 상당 부분 검사기에 기대고 있어요. 그래서 워털루대 마이클 루빈스타인(Michael Rubinstein)은 Lean 기본 커널뿐 아니라 따로 만든 검사기 여러 종으로 다시 돌려 모두 통과시켰는데요. 번스타인도 여러 검사기를 돌리는 건 한 프로그램의 버그를 메울 수 있다며 권하지만, 검사기들이 같은 버그를 공유하는 경우도 있어 공격을 막는 효과는 분명하지 않다고 봤어요. 그는 검사기 자체가 옳게 작동한다는 증명이 더 나은 답이라며, 그런 증명을 받은 HOL Light 복제판 캔들(Candle)을 예로 들었어요.

다만 이 목록은 리만 증명을 직접 다루지 않고, 리만 증명에서 버그가 악용됐다는 근거도 없어요. 번스타인 스스로도 빠진 보고가 있을 수 있다고 적었어요.
