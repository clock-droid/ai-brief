---
title: "리만 가설 증명 소동, 무엇이 확인됐고 무엇이 남았나"
date: 2026-11-23T13:30:00+09:00
category: science
format: 해설
summary:
  - "11월 20일 알푀게가 Claude와 함께 리만 가설 증명을 Lean 코드로 공개했고, 22일 Lean·Mathlib 커뮤니티가 맞다고 확인함."
  - "같은 날 스탠퍼드 쪽도 인간 단독 증명 초안을 공개했지만, 이쪽은 문제점 지적이 나오는 중임."
  - "남은 쟁점은 문제를 코드로 옮긴 부분의 확인과, 사람이 이해할 수 있는 버전임."
sources:
  - name: The Decoder — Lean and Mathlib community officially confirms
    url: https://the-decoder.com/lean-and-mathlib-community-officially-confirms-levent-alpoges-proof-of-the-riemann-hypothesis-is-correct/
  - name: The Decoder — Stanford releases an all-human competing draft
    url: https://the-decoder.com/hours-after-anthropic-claims-a-claude-proof-of-the-riemann-hypothesis-stanford-releases-an-all-human-competing-draft/
---

주) 위 두 기사에 나온 내용만 정리함. 수학 내용 자체를 설명하지는 않음.

## 0) 개요

결론부터 말하면, "기계가 검사한 증명"은 나왔고 "사람이 이해한 증명"은 아직 없어. Lean이 뭔지, 왜 그게 중요한지는 아래에서 풀게.

## 1) 무슨 일이 있었나

- 11월 20일(금) 알푀게(Levent Alpöge)가 Claude와 함께 쓴 리만 가설 증명 논문과 코드를 자기 웹사이트에 올렸음.
- 리만 가설은 1859년에 제시된 문제로, 클레이 수학연구소의 밀레니엄 문제라서 상금이 100만 달러 걸려 있음.
- 방법은 수학자 스테파노프(Stepanov)의 아이디어를 넓힌 것임. 특수 변환을 사슬처럼 이어 미분 효과를 흉내 냈고, 길이 X인 수열에 대해 사슬 길이가 X의 제곱근이어야 한다는 핵심 통찰을 Claude가 냈다고 함.
- 같은 날 몇 시간 뒤 스탠퍼드의 라비 바킬(Ravi Vakil)이 알레산드로 마술로(Alessandro Masullo)의 인간 단독 증명 초안을 블로그에 공개했음. 원래 1년 더 다듬을 계획이었는데 발표가 겹쳐 앞당겼다고 함.

## 2) Lean이 뭐고, 확인은 어디까지 됐나

Lean은 증명을 코드로 쓰면 컴퓨터가 한 단계씩 맞는지 검사해주는 도구야. 사람이 수십만 쪽을 읽지 않아도 돼.

- 증명 코드는 약 1,700만 줄임. 인쇄하면 25만 쪽 넘는다고 함.
- 22일 Lean·Mathlib 커뮤니티가 공식 성명을 냈음: "We have full confidence that Alpöge's proof is correct" (증명이 맞다고 확신한다).
- 수십 명이 코드를 독립적으로 돌려 같은 결과를 얻었고, MIT의 앤드루 서덜랜드(Andrew Sutherland)가 독립 검증 항목을 정리해 올렸음.
- 반면 스탠퍼드 초안은 여러 사람이 AI 모델의 도움으로 문제점을 지적하는 중이라고 바킬이 업데이트했음.

## 3) 그래서 뭐가 달라지나

Q: 이제 리만 가설은 확정된 거야?
A: 아니야. 기사들은 두 증명 모두 커뮤니티 검토가 끝나기 전에는 받아들여진 게 아니라고 해. Lean 검증이 통과해도, 원래 문제를 코드로 옮길 때 실수가 있었다면 증명은 무효일 수 있어. 이 부분은 전문가가 비교적 쉽게 확인할 수 있다고 함.

Q: 사람이 이해할 수는 있어?
A: 알푀게가 몇 달 안에 더 짧고 읽을 수 있는 버전을 쓰겠다고 했고, 일부 세부 분야는 아직 자기도 완전히 이해하지 못한다고 인정했어.

Q: 맞다면 뭐가 바뀌어?
A: 리만 가설에 기대는 수백 편의 논문이 조건부 결과에서 정리로 바뀐다고 함.

Q: 홍보 아니야?
A: 발표 시점이 Anthropic 상장 직후라 "unfortunate"하다고 알푀게가 인정했지만, 홍보용이라는 의혹은 부인했음.

※ 쉽게 보이려고 많이 줄여 설명했음. 정확한 내용은 원문과 알푀게의 논문을 볼 것.
