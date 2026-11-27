---
title: "GPT-6.2, 상대 모델보다 '덜 생각한다' 측정"
date: 2026-11-27T11:14:00+09:00
category: models
sources:
  - name: micjm — OpenAI may be in cost control mode
    url: https://micjm.com/blog/openai-is-in-cost-control-mode/
    published: 2026-11-26T00:00:00+00:00
  - name: GeekNews — OpenAI가 비용 통제에 나섰을까? GPT-6.2의 추론 토큰 감소
    url: https://news.hada.io/topic?id=37922
    published: 2026-11-26T22:33:47+00:00
figure:
  src: https://micjm.com/blog/openai-is-in-cost-control-mode/reasoning-tokens-vs-opponents.png
  alt: "가로축은 상대 모델의 과제당 추론 토큰 중앙값, 세로축은 해당 모델의 추론 토큰 중앙값인 산점도. 아스트라 6에서 6.2, 솔 6.1에서 6.2로 가는 화살표가 같은 토큰 대각선 아래로 크게 벗어나 있음"
  caption: "과제당 추론 토큰 중앙값을 같은 과제의 상대 모델과 비교한 그림. GPT-6.2 아스트라·솔이 대각선 한참 아래로 벗어남"
  credit: micjm
  url: https://micjm.com/blog/openai-is-in-cost-control-mode/
  width: 1232
  height: 1294
---

OpenAI의 GPT-6.2 아스트라(Astra)와 솔(Sol)이 전작보다 과제당 '생각하는 양'이 눈에 띄게 줄었다는 외부 측정이 나왔어요. 같은 일을 두 모델에 맡겨 결과를 겨루게 하는 오픈소스 시스템 '에이전트 듀얼(Agent Duel)' 기록을 분석한 블로그 micjm은 26일, 두 모델이 비용을 아끼는 쪽으로 조정된 것으로 보인다고 주장했어요.

추론 토큰은 모델이 답을 내기 전 속으로 따져 보는 데 쓰는 글자 단위예요. 많이 쓸수록 비용이 들지만 어려운 문제는 더 잘 풀리는 경향이 있는 것. 분석에 따르면 아스트라 6과 솔 6.1은 같은 과제를 받은 상대 모델과 추론 토큰 사용량이 비슷했는데, 6.2 두 모델은 상대보다 유독 적게 쓰는 '이상치'가 됐어요. 그림을 보면 상대가 과제당 약 6,000개를 쓸 때 솔 6.2는 수백 개 수준이에요. 감소가 우연일 확률(p값)은 추론 토큰 기준 솔 0.00013, 아스트라 0.0064, 출력 토큰 기준 솔 0.0055, 아스트라 0.022로 모두 0.05보다 작았다고 해요.

OpenAI는 같은 날 출시 때 요금 계산 실수로 구독 한도가 덜 깎였다며 이를 고쳤다고 밝혔는데요, 이번 측정은 구독 한도가 아니라 모델이 과제마다 실제로 쓰는 토큰 양을 본 거예요. 다만 작성자도 "비용 조정된 것으로 보인다"는 추정으로 썼을 뿐, 토큰 수만으로는 OpenAI의 실제 운영 비용이나 변경 이유를 알 수 없어요. 개인이 운영하는 시스템의 투표 기록이고, 검정마다 표본 크기도 글에 밝히지 않았어요.
