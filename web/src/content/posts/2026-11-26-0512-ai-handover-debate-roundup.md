---
title: "'AI에 결정권 넘기기' 논쟁 3주 정리 (11월 28일 기준)"
date: 2026-11-26T05:12:00+09:00
category: safety
format: 정리
updated: 2026-11-28T15:15:00+09:00
summary:
  - "11월 들어 올트먼·브록먼, 알렉산더 왕, 보아즈 바락이 잇달아 '인류가 AI에 사회의 통제권을 점진적으로 넘기는 것'에 반대한다고 밝혔다."
  - "25일 악시오스가 '앤트로픽 내부에선 초지능에 결정권 일부를 넘기자는 시각이 흔하다'고 보도하자, 아모데이는 'AI 통치는 끔찍한 생각'이라며 경쟁사들의 '분위기 포지셔닝'을 비판했다."
  - "술레이만은 아모데이에 동의했고 마커스 등은 'AI 개발 자체가 민주적이지 않다'고 되물었다. 25일엔 블로거 잭 디스페인 저우가 스콧 알렉산더의 이양 찬성론을 '선한 신도 누군가를 지게 만든다'며 장문으로 반박해, 논쟁이 연구소 밖 지식인 사이로 번졌다. 28일엔 OpenAI의 데이비드 옥스가 '이양은 주장 없이 이미 일어나고 있다'고, 세브 크리어가 '주체성 상실과 정당한 위임을 구분하자'고 써 논쟁의 틀 자체를 문제 삼았다."
sources:
  - name: X (@sebkrier)
    url: https://x.com/sebkrier/status/2126466641387003981
    published: 2026-11-28T00:02:09+00:00
  - name: X (@davideoks)
    url: https://x.com/davideoks/status/2126425483013132755
    published: 2026-11-27T21:18:36+00:00
  - name: Sulat — Amodei rejects handing AI human free will, answers Axios
    url: https://news.sulat.com/2026/11/26/amodei-ai-free-will/
  - name: 유튜브 — New York Times Podcasts (딜북 서밋 대담)
    url: https://www.youtube.com/watch?v=3HwMSP0nUEA
    published: 2026-11-23T11:16:32+00:00
  - name: X (Alexandr Wang)
    url: https://x.com/alexandr_wang/status/2124636606959345776
    published: 2026-11-22T22:50:15+00:00
  - name: Windows On Theory (Boaz Barak) — Human empowerment in a few fake graphs
    url: https://windowsontheory.org/2026/11/23/human-empowerment-in-a-few-fake-graphs/
    published: 2026-11-23T15:14:58+00:00
  - name: Novara Media — 테그마크 인터뷰
    url: https://novaramedia.com/2026/11/24/anthropic-staff-openly-talk-about-taking-over-the-world-claims-top-mit-physicist/
    published: 2026-11-24T15:51:27+00:00
  - name: Axios — Rival AI leaders push back against Anthropic vision of surrendering human agency to AI
    url: https://www.axios.com/2026/11/25/anthropic-ai-human-control-debate-free-will
    published: 2026-11-25T10:01:00+00:00
  - name: TIPP Insights — AI Executives Divided Over Human Control
    url: https://tippinsights.com/ai-executives-divided-over-human-control-in-the-age-of-superintelligence/
    published: 2026-11-25T10:32:00+00:00
  - name: X (@DarioAmodei)
    url: https://x.com/DarioAmodei/status/2125656399392690605
    published: 2026-11-25T18:22:33+00:00
  - name: MLQ.ai — Amodei calls turning over governance to AI 'a terrible idea'
    url: https://mlq.ai/news/amodei-calls-turning-over-governance-to-ai-a-terrible-idea/
    published: 2026-11-25T19:26:00+00:00
  - name: Techmeme — Axios 후속 보도 요약
    url: https://www.techmeme.com/261125/p31#a261125p31
    published: 2026-11-25T19:45:01+00:00
  - name: X (@mustafasuleyman)
    url: https://x.com/mustafasuleyman/status/2125673700032905321
    published: 2026-11-25T19:31:17+00:00
  - name: X (@garymarcus)
    url: https://x.com/garymarcus/status/2125674788572315713
    published: 2026-11-25T19:35:37+00:00
  - name: X (@garrisonlovely)
    url: https://x.com/garrisonlovely/status/2125672873033371729
    published: 2026-11-25T19:28:00+00:00
  - name: Tracing Woodgrains — Spitting in the Face of Glaude
    url: https://www.tracingwoodgrains.com/p/spitting-in-the-face-of-glaude
    published: 2026-11-25T00:00:00+00:00
  - name: Simon Willison — Quoting Jack Despain Zhou
    url: https://simonwillison.net/2026/Nov/26/jack-despain-zhou/
    published: 2026-11-26T15:09:31+00:00
---

주) 11월 초부터 26일 새벽(한국 시간)까지, "초지능이 오면 인류가 사회의 결정권을 AI에 넘기게 될까, 넘겨도 될까"를 두고 AI 업계 인사들이 공개적으로 한 말과 보도를 날짜순으로 모았어요. 발언 대부분은 의견이고, 악시오스의 내부 보도는 익명 소식통 기준이에요.

이 논쟁의 배경엔 '점진적 이양(gradual handover)'이라는 생각이 있어요. AI가 사람보다 나은 판단을 하게 되면 경제·정책 결정이 하나둘 AI로 넘어가는 게 자연스럽고 어쩌면 바람직하다는 시각이에요. 리만 가설·VP≠VNP 같은 AI 증명이 잇달아 나오며 "초지능이 가깝다"는 말이 늘자, 이 시각을 둘러싼 입장 표명도 함께 늘었어요.

1. **올트먼 "사람이 언제나 미래를 통제해야"** (11월 4일, X)
   샘 올트먼(Sam Altman) OpenAI CEO가 X에 "사람은 언제나 미래를 통제해야 한다"고 썼어요. 특정 회사를 겨냥하진 않았지만, 뒤의 논쟁에서 '통제' 진영의 대표 발언으로 계속 인용돼요.
   ▶ 14일 후 — 11월 18일 뉴욕타임스 딜북 서밋에서 올트먼과 그레그 브록먼(Greg Brockman)은 실리콘밸리에서 늘고 있는 '점진적 이양' 이야기를 둘 다 끔찍한 생각이라고 했어요. 진행자가 "사람이 루프 안에(in the loop)"라고 하자 올트먼은 "루프 안이 아니라 통제(in control)"라고 고쳐 말했어요 (23일 팟캐스트 공개).

2. **알렉산더 왕 "사회를 AI에 넘기는 걸 받아들여선 안 돼"** (11월 22일, X)
   메타(Meta)의 AI 책임자 알렉산더 왕(Alexandr Wang)은 리만 가설 증명을 초지능이 오고 있다는 신호로 보면서도, 사회를 AI에 '넘겨주는(handover)' 것을 받아들여선 안 되고, 그게 불가피하다는 생각은 "게으른 사고"라고 했어요. 강한 AI를 인정하는 쪽에서도 이양에는 반대한다는 점이 이 발언의 무게예요.

3. **보아즈 바락 "통제권 넘길 필요 없다, 조절할 건 속도"** (11월 23일, 블로그)
   하버드대 교수이자 OpenAI 연구원 보아즈 바락(Boaz Barak)은 AI를 개인 한 명이 아니라 문자·시장·제도로 커져 온 '인류 전체의 지능'과 비교해야 한다며, AI가 사람보다 똑똑해지면 통제권을 넘길 수밖에 없다는 논리에 반대했어요. 제한해야 할 건 AI 지능의 절대 수준이 아니라 발전 속도라고 주장했어요 (개인 의견이라고 밝힘).

4. **테그마크 "앤트로픽 직원들, 술자리서 세계 장악 이야기"** (11월 24일, 노바라 미디어)
   MIT 물리학자 맥스 테그마크(Max Tegmark)는 앤트로픽(Anthropic) 직원들이 '쿠데타' 대신 '통제 없는 정렬(alignment without control)'이란 말을 쓴다며, 사람이 끌 수 없는 AI에 가치를 심어 맡기는 구상이라고 해석했어요. 사적 대화에 대한 본인 전언이고, 앤트로픽 반응은 실리지 않았어요. 이때부터 논쟁의 과녁이 앤트로픽으로 좁혀져요.
   ▶ 1일 후 — 아래 악시오스 보도로 이어져요.

5. **악시오스 "앤트로픽 안에선 이양 시각이 흔해"** (11월 25일, 악시오스)
   악시오스(Axios)의 매디슨 밀스(Madison Mills)는 내부 논의를 아는 사람들을 인용해, 인류가 결국 결정권 일부를 초지능에 넘길 가능성이 크고 많은 경우 바람직하다는 시각이 앤트로픽 안에서 흔하다고 보도했어요. 이름이나 규모는 밝히지 않았어요. 경쟁사 경영진이 앤트로픽을 지목하지 않은 채 반대 목소리를 내고 있고, 일부는 이런 이야기가 대중·정치권 반감을 키울까 봐 사석에서 불만을 나타냈다고도 했어요. 앤트로픽 대변인은 아모데이가 여러 차례 인간의 AI 통제를 지지해 왔고, 클로드(Claude)는 인간의 감독을 해치지 않도록 학습된다고 답했어요.
   ▶ 같은 날 — 다리오 아모데이(Dario Amodei) CEO가 X에 긴 반박 글을 올렸어요. AI에 "인간의 자유 의지를 넘기자"고 생각한다는 건 "터무니없다"며, 자기 에세이 수백 쪽의 일관된 주제가 "AI는 정당한 민주적 절차로 다스려져야 한다"는 것이라고 했어요. AI 통치는 "끔찍한 생각"이고, "효율이나 안보를 위해 정당성과 자기결정권을 희생해선 안 된다"고 썼어요. 다만 운전·항암제 설계·소프트웨어 작성처럼 특정 작업의 자동화는 별개 문제라며 자기 생각이 "엇갈린다"고 했어요. AI가 다음 세대 AI를 완전히 자율로 만드는 건 아직 안전하지 않다는 앤트로픽의 11월 초 입장을 다시 들었고, 일자리 충격이 크면 일부 배포를 늦출 수도 있다고 했어요. 그리고 구호만 되풀이하는 일부 CEO를 "분위기에 기댄(vibes-based) 상업적·정치적 포지셔닝"이라고 비판했어요.
   ▶ 같은 날 — 무스타파 술레이만(Mustafa Suleyman) 마이크로소프트 AI CEO는 "구호는 가드레일이 아니다"라며 아모데이에 동의하고, 자신들의 '휴머니스트 AI 행동 강령'을 구체화의 첫걸음으로 들었어요. 개리 마커스(Gary Marcus)도 아모데이 말에 동의하면서, 지금 AI 개발 자체가 사실상 민주적 절차를 거치지 않는다고 짚었어요. 기자 개리슨 러블리(Garrison Lovely)는 "미국 대중이 민주적으로 결정한다면 자기 노동을 대체할 기술을 만들자고 하겠느냐"는 질문을 던졌어요.

## 현황 (11월 26일 05시 기준)

공개적으로 "AI에 사회의 통치를 넘기자"고 말한 AI 기업 경영진은 지금까지 없어요. 올트먼·브록먼·왕·바락·아모데이 모두 그 반대를 말했어요. 갈리는 지점은 두 가지예요. 하나는 앤트로픽 내부 분위기에 대한 악시오스·테그마크의 전언이 사실이냐인데, 아모데이는 자기 입장을 밝혔을 뿐 "내부에 그런 시각이 흔하다"는 보도 내용 자체는 직접 다루지 않았어요. 다른 하나는 아모데이가 그은 선, 즉 '통치'는 안 되지만 '작업 자동화'는 경우에 따라 된다는 구분이 어디서 끊기느냐예요. 마커스·러블리의 질문처럼, 비판은 이제 "누가 그 선을 정하느냐"로 옮겨 가고 있어요.

악시오스 원문과 아모데이 트윗 전문은 유료·로그인 벽에 막혀, TIPP 인사이트·MLQ.ai·Sulat 등이 옮긴 내용과 Techmeme 요약 기준이에요.

## 11월 27일 15시

6. **저우 "어떤 단일한 의지에도 미래를 맡겨선 안 돼"** (11월 25일, 트레이싱 우드그레인스)
   블로거 잭 디스페인 저우(Jack Despain Zhou)가 '글로드의 얼굴에 침 뱉기'라는 장문으로 이양 찬성론을 정면으로 반박했어요. 과녁은 경영진이 아니라 스콧 알렉산더(Scott Alexander)의 글 '이양 반대에 대한 반대(Against Against Handover)'예요. 알렉산더는 완전히 정렬된 AI라면 "우주를 알아서 배치해 달라"고 맡겨도 되지 않냐고 물었는데요. 저우는 이 가상의 선한 신을 '글로드(Glaude)'라 부르며, 예루살렘 소유권처럼 모두가 만족할 답이 없는 문제에선 아무리 선한 신도 누군가를 지게 만든다고 봤어요. 앤트로픽에 대해선 "무섭다"면서도 OpenAI·xAI·딥마인드·딥시크도 똑같이 무섭다고 했고, 직원들을 선의의 사람들로 보지만 그들이 권력 게임을 하고 있다는 걸 인정하길 바란다고 했어요. 다만 멸종이 거의 확실하다는 비관론과 AI 개발의 영구 중단에도 반대해, '사람이 따라갈 수 있는 속도로 영구히 조절하자'는 쪽에 섰어요 (이 사이트의 원문 요약 참고).
   ▶ 1일 후 — 사이먼 윌리슨(Simon Willison)이 26일 이 글 가운데 AI가 글쓰기를 '탈개인화'한다는 대목을 블로그에 옮기며 퍼졌어요.

**현황 추가 (11월 27일 15시)**
- 논쟁이 AI 기업 경영진의 입장 표명에서 연구소 밖 블로거·지식인의 장문 논쟁으로 넓어졌어요. 찬성 쪽 논리를 가장 분명히 편 알렉산더의 글이 반박의 과녁이 됐어요.
- 알렉산더 쪽의 재반박이나 앤트로픽의 추가 입장은 아직 확인되지 않았어요.

## 11월 28일 15시

7. **옥스 "이양은 아무도 주장하지 않아도 이미 일어나고 있다"** (11월 27일, X)
   OpenAI에서 일하는 데이비드 옥스(David Oks)가 지금의 '이양(handover)' 논쟁이 헛다리를 짚고 있다고 썼어요. '사회를 AI에 넘기자'고 대놓고 주장하는 사람은 거의 없는데, 사람들이 편해서 신문 기사·정치 연설·법안 작성을 AI에 맡기는 일은 이미 세계 곳곳에서 벌어지고 있다는 것. 아무도 옹호하지 않아도 일어나는 이 과정이 '점진적 무력화(gradual disempowerment)'의 실제 모습이라며, 99%가 직관적으로 반대하는 생각과 싸우기보다 무엇을 넘기고 무엇을 지킬지 따지자고 했어요.
   ▶ 0일 후 — 세브 크리어(Séb Krier)가 이 글을 받아, 논쟁이 '주체성 상실'과 '정당한 위임'을 뒤섞는다는 장문을 올렸어요. 철학자 조지프 라즈(Joseph Raz)의 권위 이론을 빌려, 따르는 편이 스스로 판단할 때보다 자기 이유에 더 맞으면 맡기는 건 정당하지만 도덕적 신념처럼 과정 자체가 중요한 영역은 예외라고 봤어요. 맡기더라도 되돌리고 빠져나올 장치, AI가 개발사가 아니라 사용자의 이유를 따르게 할 장치가 있어야 한다고 했어요.

**현황 추가 (11월 28일 15시)**
- 논쟁의 축이 '넘길 것인가 말 것인가'에서 '무엇을, 어떤 조건으로 맡기는가'로 옮겨 가는 흐름이에요. 옥스는 OpenAI 소속으로 1번 올트먼과 같은 회사지만, 경영진의 '통제권 반대' 선언보다 이미 진행 중인 일상적 위임을 문제로 봤어요.
- 알렉산더 쪽의 재반박이나 앤트로픽의 추가 입장은 아직 확인되지 않았어요.
