---
title: "앤트로픽, API를 파이썬→러스트로…CPU 70%↓, 검증은 클로드 팀이"
date: 2026-11-26T03:11:00+09:00
category: agents
sources:
  - name: Anthropic — Migrating the Messages API to Rust
    url: https://www.anthropic.com/research/migrating-api-to-rust
    published: 2026-11-25T16:26:00+00:00
  - name: X (@AnthropicAI)
    url: https://x.com/anthropicai/status/2125627317263466739
  - name: Techmeme
    url: https://www.techmeme.com/261125/p26#a261125p26
    published: 2026-11-25T17:05:04+00:00
tweet:
  author: Lance Martin
  handle: rlancemartin
  text: "we recently migrated the Claude Messages API from Python to Rust. in this new eng blog, we share how we used the Python API as an oracle, set up verification loops, and had a team of agents fix diffs until Rust matched production's observable behavior. https://t.co/IFqXTXZybM"
  url: https://x.com/rlancemartin/status/2125627070084796562
post: 2026-11-26-0311-anthropic-rust-migration-summary
figure:
  src: https://assets.claude.com/7de2a8325622d82fedbce7ef4ff369b2e27c3042.png?w=1920&q=75&fm=webp&fit=max
  alt: "4월 말부터 8월까지 러스트 버전 입력이 파이썬과 일치한 비율을 그린 선 그래프. 24%에서 5월 초 6.5%로 떨어졌다가 수정이 배포되며 급히 올라 99.6%에서 끝남"
  caption: "러스트 버전의 입력 처리가 기존 파이썬과 같은 결과를 낸 비율. 5월 초 6.5%에서 8월 99.6%까지 올라감"
  credit: Anthropic
  url: https://www.anthropic.com/research/migrating-api-to-rust
  width: 1920
  height: 1192
---

앤트로픽(Anthropic)이 클로드(Claude)를 부르는 주 통로인 메시지 API(Messages API)를 파이썬(Python)에서 러스트(Rust)로 통째로 다시 짰다고 11월 25일 공개했어요. 요청당 CPU 사용은 약 70%, 메모리는 80% 넘게 줄었고 첫 토큰이 나오기까지 걸리는 시간(중앙값)도 약 20% 짧아졌다고 해요. 앤트로픽이 강조한 건 성능보다 "새 코드가 옛 코드와 똑같이 동작한다는 걸 어떻게 증명했나"예요.

**왜 다시 짰어?**

이 API는 2023년 파이썬으로 만들었어요. 처음엔 요청을 모델에 넘겨주기만 했는데, 점점 요청 검사·프롬프트 조립·토큰화·안전 분류기·출력 해석까지 맡게 됐는데요. 그 사이 트래픽은 2024년 초부터 2026년 가을까지 약 1,800배로 늘었어요. 출력 해석 부분만 러스트로 바꿨더니 CPU가 8~10% 줄었지만, 토큰 하나가 두 언어 사이를 세 번 오가는 비용이 생겨 전부 바꾸기로 했다는 것. 클로드가 핵심 경로의 첫 버전을 쓰는 데는 약 일주일이면 됐다고.

**진짜 어려운 건 검증이었어**

기존 통합 테스트 약 700개로는 부족했어요. 테스트를 러스트로 옮기는 과정에서 검사 조건이 느슨해진 곳이 100개 넘게 나왔고, 선택지 20개만 켜고 꺼도 조합이 100만 개를 넘었어요. 4월에 러스트 버전은 테스트의 약 98%를 통과했지만 실제 요청과 결과가 같았던 건 4분의 1 정도였어요. 그래서 운영 중인 파이썬 API 자체를 '정답지(oracle)'로 삼고, 실제 트래픽을 러스트에도 똑같이 흘려 단계별로 비교했어요. 차이가 나면 사용자 글 없이 "어느 단계, 몇 번째 바이트"만 담은 '지문'을 남기고, 클로드 에이전트 팀이 지문별로 원인을 찾아 고치게 했다는 것. 일치율은 5월 초 6.5%에서 99.6%까지 올랐고, 9월에 공개 트래픽이 러스트로 넘어갔어요.

**어디까지 믿어도 돼?**

모든 수치는 앤트로픽 자체 측정이에요. 앤트로픽 스스로도 검증기는 "결과가 같은지"만 알려 줄 뿐 고친 방식이 좋은지는 판단하지 못해, 에이전트가 가장 싼 땜질을 고르는 경우가 있었고 사람 검토가 계속 필요했다고 밝혔어요.
