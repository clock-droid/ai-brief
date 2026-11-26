---
title: "AI가 한 달 새 건드린 수학·이론CS 난제 정리 (11월 26일 기준)"
date: 2026-11-25T11:11:00+09:00
category: science
format: 정리
updated: 2026-11-26T09:15:00+09:00
summary:
  - "OpenAI가 11월 24일 논문 9편을 한꺼번에 올리며 행렬 곱셈 지수 9/4 확정, 스메일 9번 문제(강다항 LP) 해결, 다항 허쉬 추측 반증, VP≠VNP 위계 전체 분리, 푸리에 변환 게이트 수 결정을 주장했다."
  - "23일엔 유판 류가 양자 대화형 증명은 메시지 두 번이면 충분하다는 'QIP(2)=PSPACE' 원고를 냈고, 애런슨은 AI 도움이 이제 눈썹 하나 까딱하지 않을 만큼 일상이 됐다고 전했다."
  - "대부분 AI가 쓰고 일부만 Lean으로 형식화됐으며 사람 검토는 진행 중이다. 애런슨은 25일 '처음으로 P≠NP 증명이 멀지 않았다고 느낀다'고 썼고, 리만 증명을 사람이 읽을 판으로 풀자는 폴리매스가 시작된 가운데 25일엔 1,700만 줄이던 Lean 증명을 7만 6,000줄로 줄인 압축판이 나왔다."
sources:
  - name: OpenAI Math — 공개 이력(history)
    url: https://github.com/openai/math/blob/main/history.md
    published: 2026-11-25T00:18:47+00:00
  - name: OpenAI Math — README
    url: https://github.com/openai/math/blob/main/README.md
    published: 2026-11-25T00:18:47+00:00
  - name: OpenAI Math — The matrix multiplication exponent is nine fourths (논문)
    url: https://github.com/openai/math/blob/main/preprints/The-matrix-multiplication-exponent-is-nine-fourths-November-24-2026/paper.pdf
    published: 2026-11-25T00:18:47+00:00
  - name: OpenAI Math — Strongly polynomial linear programming (논문)
    url: https://github.com/openai/math/blob/main/preprints/Strongly-polynomial-linear-programming-November-24-2026/paper.pdf
    published: 2026-11-25T00:18:47+00:00
  - name: OpenAI Math — Superpolynomial graph diameter of simple polytopes (논문)
    url: https://github.com/openai/math/blob/main/preprints/Superpolynomial-graph-diameter-of-simple-polytopes-November-24-2026/paper.pdf
    published: 2026-11-25T00:18:47+00:00
  - name: Anthropic formal-math — VP ≠ VNP (GitHub)
    url: https://github.com/anthropics/formal-math/tree/main/vp-vnp
    published: 2026-11-23T23:31:40+00:00
  - name: The Decoder — Lean·Mathlib 커뮤니티, 알푀게 증명 확인
    url: https://the-decoder.com/lean-and-mathlib-community-officially-confirms-levent-alpoges-proof-of-the-riemann-hypothesis-is-correct/
    published: 2026-11-22T11:08:31+00:00
  - name: Shtetl-Optimized (Scott Aaronson)
    url: https://scottaaronson.blog/?p=10362
    published: 2026-11-24T23:17:20+00:00
  - name: Shtetl-Optimized (Scott Aaronson) — HOLY SHIT HOLY SHIT HOLY SHIT HOLY SHIT
    url: https://scottaaronson.blog/?p=10379
    published: 2026-11-25T19:01:13+00:00
  - name: arXiv — Two messages suffice for quantum interactive proof systems (Yupan Liu)
    url: https://arxiv.org/abs/2611.31236
    published: 2026-11-23T18:59:31+00:00
  - name: Terence Tao 블로그 — G.R.H. Polymath (Sahai·Sawin·Silberman 기고)
    url: https://terrytao.wordpress.com/2026/11/24/g-r-h-polymath/
    published: 2026-11-25T05:29:41+00:00
  - name: X (@1337isnot1337) — Caiolo–Ferroni–Hoster conjecture is false
    url: https://x.com/1337isnot1337/status/2125235237471080565
    published: 2026-11-24T14:29:00+00:00
  - name: GitHub — lsernau/grh-lean (README)
    url: https://github.com/lsernau/grh-lean
  - name: GeekNews — Anthropic의 일반화 리만 가설 Lean 증명, 7만 6,000줄로 압축
    url: https://news.hada.io/topic?id=37854
    published: 2026-11-25T23:31:57+00:00
  - name: itsdavis.com — Solved mathematical conjectures
    url: https://itsdavis.com/solved-conjectures/
  - name: arXiv — Dual Chow polynomials of matroids and posets
    url: https://arxiv.org/abs/2605.28474
    published: 2026-05-27T00:00:00+00:00
---

주) 10월 초부터 11월 24일까지 AI 연구소가 공개한 수학·이론 컴퓨터과학 결과 가운데, 오래된 공개 난제를 건드린 것만 날짜순으로 모았어. 전부 "주장" 단계이고, 사람 전문가의 검토가 끝난 건 아직 없어.

1. **행렬 곱셈 지수 9/4 상한** (10월 2일, OpenAI Math 저장소)
   OpenAI 내부 모델이 n×n 행렬 두 개를 대략 n^(9/4)번 연산으로 곱할 수 있다는 상한을 냈어. 행렬 곱셈 지수 ω(오메가)는 "n×n 행렬 곱에 드는 연산 수가 n의 몇 제곱으로 늘어나나"를 뜻하는 수야. 교과서 방식은 3이고, 슈트라센(Strassen)의 '곱셈 7번' 공식 이후 이 지수를 얼마나 낮출 수 있느냐가 오랜 질문이었지.
   ▶ 53일 후 — 11월 24일 OpenAI가 맞는 하한까지 증명했다고 발표했어. n≥2마다 곱셈·나눗셈 게이트가 적어도 ⌈n^(9/4)/2⌉개 필요하다는 거야. 상한은 다른 연구자들(Amanov·van den Berg·Zuiddam)이 모든 체로 넓혀 둔 상태였으니, 위아래가 맞물려 **ω = 9/4로 확정**됐다는 주장이 돼. 많은 사람이 믿던 "ω = 2" 추측은 틀린 게 되는 셈이고. 논문 요약은 "더 작은 지수가 가능하다면 텐서 네트워크를 너무 많이 압축할 수 있게 되어, 목록 원소가 모두 다른지 검사하는 문제의 알려진 하한과 모순된다"는 식이야.

2. **지수 시간 가설(ETH) 반증** (10월 26일, OpenAI)
   ETH(Exponential Time Hypothesis)는 "3-SAT 같은 문제는 지수 시간보다 빨리 못 푼다"는, 복잡도 이론의 많은 결과가 기대던 가정이야. OpenAI는 고정 폭 CNF 공식의 해 개수를 준지수 시간·다항 공간에 정확히 세는 결정론적 알고리즘을 냈다고 했어.
   ▶ 같은 날 — 러셀 임팔리아초(Russell Impagliazzo), 라모한 파투리(Ramamohan Paturi), 라이언 윌리엄스(Ryan Williams)가 이끄는 독립 작업반이 증명을 검토·해설하기로 했고, OpenAI는 작업반 요청으로 자료를 바로 공개했어.
   ▶ 약 4주 후 — 스콧 애런슨(Scott Aaronson)은 블로그에서 이 반증을 보고 P≠NP에 대한 자기 확신을 97%에서 95%로 낮췄었다고 밝혔어.

3. **리만 가설 증명** (11월 20일, 레벤트 알푀게(Levent Alpöge)·Claude)
   앤트로픽 소속 수학자 알푀게가 Claude와 함께 Lean으로 쓴 리만 가설 증명을 공개했어.
   ▶ 2일 후 — Lean·Mathlib 커뮤니티가 증명이 맞다는 "full confidence"를 공식 성명으로 밝혔어. 다만 사람이 읽을 수 있는 짧은 판은 아직 없어.

4. **VP ≠ VNP** (11월 23일, 앤트로픽 → 같은 날 OpenAI)
   VP와 VNP는 P와 NP의 '대수적 회로 버전'이야. "덧셈·곱셈 게이트로 다항식 크기 회로를 만들 수 있는 다항식"과 "그런 것들의 합으로 표현되는 다항식"이 정말 다른지 묻는 발리언트(Valiant)의 추측이고, 1970년대 말부터 P≠NP로 가는 '준비 운동'으로 여겨졌대(애런슨). 앤트로픽은 내부 Claude 모델이 찾은 증명과 Lean 형식화를 GitHub에 올렸어.
   ▶ 같은 날 — OpenAI도 "VP and VNP are different"를 공개했어. 결과 자체는 11월 6일에 얻었다고 이력에 적었어.
   ▶ 1일 후 — 11월 24일 OpenAI는 이를 넓혀 VF ⊊ VBP ⊊ VP ⊊ VNP, 즉 공식·분기 프로그램·회로·VNP 네 단계가 **모두** 서로 다르다는 논문을 냈어. 퍼머넌트(permanent) 회로 하한도 exp(c(log N)²/(log log N)²)로 올렸다고 해.

5. **스메일 9번 문제 + 다항 허쉬 추측 반증** (11월 24일, OpenAI)
   선형계획법(LP)은 하치얀(Khachiyan)의 타원체법 이후 '입력 비트 길이'에 대해선 다항 시간에 풀렸어. 그런데 숫자 크기와 상관없이 변수·제약 개수만으로 연산 횟수를 묶을 수 있느냐(강다항 시간)는 메기도(Megiddo)·타잔(Tarjan)이 묻고 스메일(Smale)이 자기 문제 목록의 9번으로 꼽은 질문이었지. OpenAI 논문은 "그렇다"고 답하는 결정론적 알고리즘을 냈다고 주장해. 볼록 2차 계획법과 평균 보상 게임까지 같이 풀린다고 하고.
   짝 논문은 정반대 방향이야. 1957년 허쉬(Hirsch)가 "면이 n개인 d차원 다면체의 두 꼭짓점은 n−d걸음이면 이어진다"고 했고, 산토스(Santos)가 43차원·면 86개 반례로 그 정확한 형태는 깼지만 "어떤 다항식으로는 묶인다"는 다항 허쉬 추측은 남아 있었어. OpenAI는 면 수의 어떤 다항식보다도 지름이 큰 단순 다면체를 만들어 이걸 반증했다고 해. 꼭짓점을 따라 걷는 심플렉스법은 다항 시간이 안 될 수 있지만, 다른 방식(강다항 LP)으로는 된다는 그림이야.

6. **해바라기 추측·푸리에 변환·정수 곱셈** (11월 24일, OpenAI)
   같은 '텐서 기하' 묶음에서 에르되시-라도(Erdős–Rado) 해바라기 추측(꽃잎 수 고정판)을 풀었다고 주장했어. 크기 k 이하 집합이 B_r^k개를 넘으면 교집합이 모두 같은 r개 집합이 반드시 있다는 거야. 또 유한 아벨 군의 푸리에 변환에 필요한 게이트 수를 N(log N)^(1/2+o(1))로 맞추고, 정수 곱셈의 '로그 지수'가 (약한 ETH 가정 아래) 1/2이라는 결과도 냈어.

7. **최소 신장 트리(MST) 결정론적 선형 시간** (11월 23일, 칸나·퍼터먼·송)
   애런슨 블로그에 따르면 산지브 칸나(Sanjeev Khanna), 에런 퍼터먼(Aaron Putterman), 쥔카이 송(Junkai Song)이 ECCC 예비 논문으로 결정론적 선형 시간 MST 알고리즘을 올렸어. 수십 년간 최선은 역아커만 함수만큼 느린 n·α(n)이었지. 저자들은 핵심 아이디어가 "전부 AI, 구체적으로 6.2 Astra가 만들었다"고 썼다고 해.
   ▶ 다만 ECCC 원문은 접속이 안 돼 직접 확인하지 못했고, 애런슨 글 기준이야.

**현황 (11월 25일 오전, OpenAI 저장소·애런슨 블로그 기준)**
- OpenAI 저장소엔 이름 없는 내부 모델이 쓴 원고 730편(375개 묶음)이 있고, 주요 결과의 약 42%가 Lean으로 형식화돼 있어. 모델에 낸 문제는 약 4,000개, 결과 하나에 평균 ChatGPT Pro 사고 시간 3시간이 들었다고 해.
- OpenAI는 이 원고들을 "다듬은 논문이 아니라 가공 전 연구 데이터"로 봐 달라고 하고, 형식화 안 된 결과엔 오류가 있을 수 있다고 미리 밝혔어. 공로와 선후 문제는 수학계 판단에 전부 맡긴다고 했고.
- Lean 검증은 "코드로 옮긴 명제"를 검사할 뿐이라, 그 명제가 논문 주장과 정확히 같은지는 사람이 따로 봐야 해. 앤트로픽 VP≠VNP 저장소도 이 대응표를 부록으로 따로 정리했어.
- 애런슨은 다음 차례로 P≠NP 자체가 나올 가능성을 "AI 회사들도 당연히 알고 있다"고 썼어. 시점은 아무도 모른다고 했고.

## 11월 25일 15시

8. **리만 증명을 '사람이 읽을 판'으로 — 폴리매스 제안** (11월 24일, 테렌스 타오 블로그)
   아누라그 사하이(Anurag Sahai), 윌 소윈(Will Sawin), 리오르 실버만(Lior Silberman)이 타오 블로그 기고로, 알푀게가 공개한 일반화 리만 가설(GRH) Lean 인증서를 여럿이 공개적으로 풀어 보자고 제안했어요. 컴퓨터가 맞다고 확인한 증명을 수학자가 이해할 수 있는 글로 옮기는 게 목표인데요. 따로 흩어진 작업을 모으고, 관련 문헌을 정리하고, 증명 속 새 수학을 더 일반적인 형태로 넓혀 보자는 것까지 네 가지를 내걸었어요. 증명이 정수론 안팎의 여러 분야에 걸쳐 있어 하위 과제로 나눌 거라고 했지만, 구조는 "아직 이르다"며 밝히지 않았어요.
   ▶ 4일 후 — 3번 항목의 "사람이 읽을 짧은 판은 아직 없다"는 상태를 풀기 위한 첫 공개 조직이 생긴 셈이에요.

9. **숫자 두 개로 "매트로이드 추측 반증" 주장** (11월 24일, X)
   신나 데이비스(Cinna Davis)는 51~53자리 음수 두 개를 올리며 카이올로·페로니·호스터가 5월에 낸 쌍대 차우 다항식(dual Chow polynomial) 추측이 틀렸다고 주장했어요. 본인 사이트엔 계수 5짜리 매트로이드에서 이 다항식이 실근을 갖지 않는다는 "제안된 반증"으로 올라 있어요. 다만 사람 수학자의 검토는 아직 없어요.

**현황 추가 (11월 25일 15시)**
- 알푀게 증명은 Lean 검증과 커뮤니티 성명까지 나왔지만, 사람이 읽을 증명은 폴리매스가 이제 만들기 시작하는 단계예요.
- X에 숫자만 올리는 식의 반증 주장도 나오고 있어, 결과마다 사람 검토와 Lean 형식화 여부를 따로 확인해야 해요.

## 11월 26일 05시

10. **QIP(2) = PSPACE** (11월 23일, 유판 류(Yupan Liu), arXiv)
   대화형 증명은 계산 능력이 약한 검증자가 능력이 무한한 증명자와 메시지를 주고받으며 주장을 확인하는 방식이에요. 양자판(QIP)이 PSPACE(다항식만큼의 메모리로 풀 수 있는 문제 전체)와 같다는 건 이미 알려져 있었고, 메시지를 3번까지 줄일 수 있다는 것도 2000년부터 알려졌어요. 2번짜리 QIP(2)는 2009년에 PSPACE 안에 들어간다는 것까지만 증명돼 같은지는 열린 문제였는데요. 류는 검증자가 얽힌 입자 쌍의 반쪽을 보내고 답 하나만 받아 확인하는 방식으로 PSPACE 전체를 검증할 수 있다며 QIP(2)=QIP=PSPACE를 주장했어요. 17쪽 단독 저자 원고이고, 논문엔 AI 사용 언급이 없어요.
   ▶ 2일 후 — 스콧 애런슨은 블로그에서 류가 AI의 도움을 받았고 그게 너무 일상이라 아무도 놀라지 않았다고 전했어요.

11. **애런슨 "P≠NP 증명이 멀지 않았다"** (11월 25일, 블로그)
   애런슨은 1번 항목의 ω=9/4 하한과 6번 항목의 푸리에 변환 결과를 24일 저녁 식탁에서 실시간으로 봤다며, "처음으로 뼛속까지 P≠NP 증명이 멀지 않았다고 느낀다"고 썼어요. OpenAI·앤트로픽이 직접 낸 증명은 반대 증거가 없는 한 맞다고 보겠다고 했고, 연구소들이 암호를 깨는 결과를 쥐고 있다는 믿을 만한 신호가 있지만 검증된 내용이 없어 소문은 퍼뜨리지 않겠다고 했어요 (이 사이트의 원문 요약 참고).
   ▶ 같은 날 — 그의 블로그 댓글에선 OpenAI 원고들을 "증명 쓰레기(proofslop)"라고 부른 반론도 나왔어요. 애런슨은 최근 논문들은 서론이 읽을 만하다고 답했어요.

**현황 추가 (11월 26일 05시)**
- 이론 컴퓨터과학 쪽 결과가 연구소 원고뿐 아니라 개인 연구자의 arXiv 원고로도 나오기 시작했어요. AI 도움을 받았는지는 논문에 적히지 않는 경우가 있어 확인이 어려워요.
- 이번 주 나온 결과 가운데 사람 전문가 검토나 학술지 심사를 마친 건 아직 없어요.

## 11월 26일 09시

12. **리만 Lean 증명 압축판: 1,700만 줄 → 7만 6,000줄** (11월 25일, GitHub 'grh-lean')
   3번 항목의 알푀게 증명을 바탕으로, 저장소 작성자가 "앤트로픽 동료들, 그리고 Claude와 협업해" 짧게 다시 만든 Lean 4 증명을 공개했어요. 리만 가설과 디리클레 L-함수의 일반화 리만 가설(GRH)을 담은 다섯 정리를 두 판으로 냈는데요. 배경 이론과 새 논증을 나누고 읽기 안내서를 붙인 읽기용 판이 약 30만 줄, 같은 정리만 담은 압축판이 약 7만 6,000줄이에요. 원본 약 1,700만 줄(인쇄하면 25만 쪽 이상)보다 200배 넘게 줄었고, Lean 기본 공리 세 개 말고는 추가 가정을 쓰지 않았다고 해요. 12코어·24GB 메모리 컴퓨터로 1~2시간이면 검사를 다시 돌릴 수 있는 크기예요.
   ▶ 1일 전 시작된 8번 항목의 폴리매스(사람이 읽을 판 만들기)가 다룰 분량이 크게 줄어든 셈이에요. 다만 README는 "기계 검사만 통과했다"며 수학자가 통독한 적도, 함께 나온 논문도 없다고 밝혔어요. 앤트로픽 공식 채널이 아니라 개인 저장소로 공개됐어요.

**현황 추가 (11월 26일 09시)**
- 리만 증명은 '맞는지'(Lean 검사·커뮤니티 성명)는 확인됐고, 이제 '읽을 수 있는지'의 단계로 넘어가고 있어요. 압축판과 읽기용 판이 나왔지만 사람의 통독·논문화는 아직이에요.
- 이번 주 나온 결과 가운데 사람 전문가 검토나 학술지 심사를 마친 건 여전히 없어요.
