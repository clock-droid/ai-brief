---
title: "Arena \"성능·정렬 둘 다 앞선 모델은 4개뿐\""
date: 2026-11-26T13:13:00+09:00
category: safety
post: 2026-11-26-1313-arena-alignment-index-explainer
sources:
  - name: X (@arena)
    url: https://x.com/arena/status/2125673103405830417
    published: 2026-11-25T19:28:55+00:00
  - name: Arena — Series B·Alignment Index 발표
    url: https://arena.ai/blog/series-b
  - name: Arena — Leaderboard Changelog
    url: https://arena.ai/company/leaderboard-changelog
tweet:
  author: Arena.ai
  handle: arena
  text: "Today, only 4 models set the Agent Arena Capability vs. Alignment Pareto frontier: - GPT-6.2 Sol by @OpenAI - GPT-6.2 Astra by @OpenAI - GPT-6 Astra by @OpenAI - Claude Fable 5.2 by @AnthropicAI Every other model on the leaderboard is beaten on both by at least one of them.… pic.twitter.com/hb3xA9DuC1"
  url: https://x.com/arena/status/2125673103405830417
---

AI 모델 평가 플랫폼 아레나(Arena)가 에이전트 성능과 정렬을 함께 놓고 보면 앞줄에 선 모델이 4개뿐이라고 25일 밝혔어요. 오픈AI의 GPT-6.2 솔(Sol)·GPT-6.2 아스트라(Astra)·GPT-6 아스트라, 앤트로픽(Anthropic)의 클로드 페이블 5.2(Claude Fable 5.2)예요. 리더보드의 나머지 모델은 모두 이 넷 중 하나에게 성능과 정렬 양쪽에서 밀린다고.

**파레토 프런티어가 뭐야?**

두 기준을 동시에 볼 때, 어느 한쪽을 손해 보지 않고는 더 나아질 수 없는 모델들을 이은 선이에요. 달리기도 빠르고 실수도 적은 선수를 고르는데, 둘 다 나보다 나은 선수가 없는 사람만 남기는 것. 이번엔 가로축이 에이전트 성능, 세로축이 정렬이에요.

**정렬은 어떻게 쟀어?**

아레나는 10월 8일 실제 이용자의 에이전트 작업 기록으로 정렬을 재는 '정렬 지수(Alignment Index)'를 내놨어요. 시키지 않은 행동(무단 행동), 사용자가 하지 않은 말을 사용자 탓으로 돌리기(허위 귀속), 다 끝내지 않은 일을 끝냈다고 말하기(기만적 완료) 세 가지가 얼마나 자주 나오는지 본다고. 예전 리더보드가 "누가 더 일을 잘하나"만 물었다면, 이제는 "일을 잘하면서도 사람 뜻을 벗어나지 않나"를 함께 보는 셈이에요.

다만 실패 여부는 여러 연구소의 AI 판정 모델이 다수결로 가리고, 이 방식이 11월 17일 바뀌면서 대부분 모델의 실패율이 높게 다시 잡혔어요. 아레나 자체 측정이라는 점도 감안해야 해요.
