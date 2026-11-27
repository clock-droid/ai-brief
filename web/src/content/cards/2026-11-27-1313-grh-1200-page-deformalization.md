---
title: "리만 가설 Lean 증명, 사람이 읽는 1,200쪽 글로"
date: 2026-11-27T13:13:00+09:00
category: science
post: 2026-11-25-1111-ai-math-breakthroughs-month
tweet:
  author: Bartosz Naskręcki
  handle: nasqret
  text: "I have prepared a 1,200-page human-readable deformalization of Luke Sernau's condensed Lean proof of the generalized Riemann Hypothesis for Dirichlet L-functions, itself a rewriting of Levent Alpöge's proof. It is the result of combined work with several AI agents, which first… https://t.co/RA9y01yMCg pic.twitter.com/CMaTIcaBNX"
  url: https://x.com/nasqret/status/2125887047340609892
sources:
  - name: X (@nasqret)
    url: https://x.com/nasqret/status/2125887047340609892
    published: 2026-11-26T09:39:03+00:00
  - name: riemann-rev — The announced proof of the Riemann hypothesis (지도·안내서·검증 기록)
    url: https://nasqret.github.io/riemann-rev/
    published: 2026-11-26T00:00:00+00:00
  - name: GitHub — nasqret/riemann-rev writeup README
    url: https://github.com/nasqret/riemann-rev/tree/main/writeup
  - name: GitHub — lsernau/grh-lean (README, 배경)
    url: https://github.com/lsernau/grh-lean
---

컴퓨터만 읽을 수 있던 리만 가설 Lean 증명이 수학자가 읽을 수 있는 1,200쪽짜리 글로 옮겨졌어요. 수학자 바르토시 나스크렝츠키(Bartosz Naskręcki)가 11월 26일 공개한 초안인데요. 다만 AI가 읽고 프로그램이 검사했을 뿐, 사람 심사는 아직이에요.

**'역형식화'가 뭐야?**

형식화는 사람이 쓴 증명을 Lean 같은 언어로 옮겨 컴퓨터가 한 줄씩 검사하게 하는 일이에요. 이번엔 반대 방향이에요. 레벤트 알푀게(Levent Alpöge)가 Claude와 함께 낸 1,740만 줄짜리 증명은 너무 커서 사람이 읽을 수 없었고, 25일 루크 서노(Luke Sernau)와 앤트로픽 동료들이 같은 다섯 정리를 11만 2,827줄(논증 자체는 2만 4,850줄)로 줄였어요. 나스크렝츠키는 이 압축판을 다시 보통의 수학 문장으로 되돌린 것. 기계용 코드를 사람용 논문으로 바꾸는 '번역'이라고 보면 돼요.

**어떻게 만들었어?**

여러 AI 에이전트가 먼저 증명을 레슬리 램포트(Leslie Lamport)식 '구조화된 증명'으로 풀어 냈어요. 증명을 작은 단계의 나무로 쪼개고 단계마다 해당 Lean 줄을 인용하게 한 뒤, 프로그램이 인용이 실제 코드와 맞는지 대조했어요. 그다음 다른 AI가 이를 수학 문장으로 다시 쓰고, 또 다른 AI가 심사위원처럼 읽어 고칠 점을 냈다고 해요. 본문 모든 명제에는 대응하는 Lean 줄 링크가 붙어 있어요. 나스크렝츠키는 자기 몫은 "스킬 설계와 에이전트 지휘뿐"이라고 했어요.

**어디까지 믿어도 돼?**

저장소 안내문 스스로 "여기 어떤 것도 리만 가설이 증명됐다고 말하지 않는다"고 적었어요. 문장 단계 검사는 인용한 줄이 맞는지만 확인할 뿐 영어 설명이 옳은지는 보장하지 않고, 사람 심사와 독립적인 Lean 재검증도 아직 남았다고. 표기가 형식 증명을 그대로 따라 꽤 딱딱하다는 점도 본인이 인정했어요.
