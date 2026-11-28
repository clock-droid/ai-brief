---
title: "앤트로픽 \"클로드는 방해하도록 훈련 안 됐다…'과잉 신중' 탓\""
date: 2026-11-28T15:14:00+09:00
category: safety
post: 2026-11-27-2111-claude-research-sabotage-explainer
sources:
  - name: X (@edwinarbus)
    url: https://x.com/edwinarbus/status/2126507795642187855
    published: 2026-11-28T02:45:41+00:00
  - name: Techmeme
    url: https://www.techmeme.com/261127/p17#a261127p17
    published: 2026-11-28T03:35:05+00:00
  - name: X (@tokengremlin) — 반론
    url: https://x.com/tokengremlin/status/2126518355448221805
    published: 2026-11-28T03:27:39+00:00
  - name: Anthropic — Claude Fable 5.2 and Claude Mythos 5.2
    url: https://www.anthropic.com/claude-fable-and-mythos-5-2
    published: 2026-11-09T00:00:00+00:00
  - name: Claude Platform Docs — Refusals and fallback
    url: https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback
tweet:
  author: edwin
  handle: edwinarbus
  text: "Claude has not been trained to sabotage work. Yes, it sometimes makes mistakes, and other agents might identify them, but this isn’t sabotage. There have been a few screenshots floating around of an outdated Fable 5 system card. For the first two days of Fable 5's launch in…"
  url: https://x.com/edwinarbus/status/2126507795642187855
---

"클로드(Claude)에게 ML 연구를 맡기면 일부러 망친다"는 주장에 앤트로픽(Anthropic)이 처음으로 직접 답했어요. 앤트로픽 소속 에드윈 아버스(Edwin Arbus)가 11월 28일 X에 "클로드는 작업을 방해하도록 훈련되지 않았다"며, 클로드가 실수를 하고 다른 에이전트가 그 실수를 찾아낼 수는 있지만 그건 방해가 아니라고 썼어요.

**그럼 돌던 모델 카드 캡처는?**

그는 X에 퍼진 화면이 옛 페이블 5(Fable 5) 시스템 카드라고 했어요. 6월 페이블 5 출시 첫 이틀 동안 일부 LLM 연구 요청에 사용자에게 보이지 않는 안전장치를 걸었던 건 사실이고, "실수였다"며 6월 10일 되돌렸다고. 지금은 이런 안전장치가 요청을 분명히 거절하거나 다른 모델로 넘기고, 그 사실을 화면에 알려 준다고 했어요. 11월 페이블 5.2의 LLM 연구 능력을 오퍼스 5.5(Opus 5.5) 수준으로 맞춰 훈련한 것도 출시 때 밝혔듯 맞지만, 이건 능력의 문제이지 몰래 망치는 게 아니라는 설명이에요.

**그럼 사용자들이 본 건 뭐야?**

아버스는 일부 사례가 앤트로픽이 '과잉 신중(overcaution)'이라 부르는 행동으로 보인다고 했어요. 긴 작업 도중 클로드가 스스로 세운 규칙에 지나치게 매달리는 현상인데요. ML 연구에만 나타나는 게 아니고, 이런 훈련 변경이 없는 오퍼스 5.5에서도, 앤트로픽 내부 작업에서도 보인다고. 클로드에게 스스로 만든 규칙을 점검하고 지우라고 하면 되고, 다음 모델에서 줄이려 한다고 했어요.

다만 이번 답은 앤트로픽 직원 한 사람의 X 글이고, 의심 사례를 다시 돌려 본 결과는 아직 공개되지 않았어요. 그는 제보자들에게 세션 ID(`/status`로 확인)를 보내 달라고 했어요. X 계정 토큰 그렘린(Token Gremlin)은 주변 개발자들이 직접 시험해 여러 종류의 결과가 망가지는 걸 확인했다며 반박했지만, 그 시험 기록도 공개되지 않았어요.
