---
title: "구글 AI가 증명했다는 '소인수분해 L[1/3]', 무슨 뜻인가"
date: 2026-11-25T23:13:00+09:00
category: science
format: 해설
summary:
  - "구글 리서치가 11월 25일 AI 에이전트 코젠틱(Cogentic)이 쓴 수학 논문 6편을 공개함. 대표 논문은 어떤 정수든 가정 없이 L[1/3] 속도로 소인수분해할 수 있다고 증명했다고 주장함."
  - "실전 최강인 일반 수체 체(GNFS)는 1990년대부터 L[1/3]로 돌았지만 그 속도는 증명되지 않은 가정에 기댔고, 가정 없이 증명된 기록은 1992년 L[1/2]가 최고였음. 이번 논문은 그 사이를 메웠다는 것."
  - "상수가 105로 GNFS(약 1.9)보다 훨씬 커서 암호를 더 빨리 깨는 방법은 아님. 동료 심사 전이고, 완성했다는 Lean 형식 증명도 아직 공개되지 않음."
sources:
  - name: Unconditional Integer Factorization in Time L_N[1/3, O(1)] (논문 PDF)
    url: https://github.com/google-research/google-research/blob/master/cogentic_research_papers/integer_factorization/paper.pdf
    published: 2026-11-25T00:00:00+00:00
  - name: Google Research GitHub — Cogentic Research Papers
    url: https://github.com/google-research/google-research/tree/master/cogentic_research_papers
    published: 2026-11-25T00:00:00+00:00
  - name: Unconditional Deterministic Subexponential Integer Factoring (논문 설명)
    url: https://github.com/google-research/google-research/tree/master/cogentic_research_papers/deterministic_factoring_l34
    published: 2026-11-25T00:00:00+00:00
  - name: OfficeChai — Google's Cogentic AI Releases Six Math Papers In One Day
    url: https://officechai.com/ai/googles-cogentic-ai-releases-six-math-papers-in-one-day-including-a-proven-fast-algorithm-for-factoring-numbers/
    published: 2026-11-25T00:00:00+00:00
  - name: 위키백과 — General number field sieve (배경)
    url: https://en.wikipedia.org/wiki/General_number_field_sieve
  - name: 위키백과 — RSA cryptosystem (배경)
    url: https://en.wikipedia.org/wiki/RSA_cryptosystem
---

주) 구글 코젠틱 논문 6편 중 소인수분해 논문 하나를 중심으로, 그 결과가 무엇을 주장하는지만 다룬다. 증명이 맞는지는 판단하지 않는다.

구글 리서치(Google Research)가 11월 25일 깃허브에 AI 에이전트 '코젠틱(Cogentic)'이 쓴 수학 논문 6편을 올렸어요. 맨 앞에 놓인 논문은 "어떤 정수든 증명된 L[1/3] 속도로 소인수분해할 수 있다"는 주장이에요. 이 글에서는 소인수분해 속도를 왜 'L[1/3]' 같은 기호로 재는지, 그래서 이번 주장이 어디에 자리하는지, 무엇을 아직 믿으면 안 되는지를 풀어 볼게요.

**소인수분해가 뭐가 어려워?**

소인수분해는 15를 3×5로 쪼개듯 어떤 수를 소수들의 곱으로 나타내는 일이에요. 작은 수는 쉽지만, 두 큰 소수를 곱한 수백 자리 수는 곱하기는 순식간인데 거꾸로 쪼개기는 엄청나게 오래 걸려요. RSA 암호가 바로 이 비대칭에 기대고 있어요. 공개된 큰 수를 쪼갤 수 있으면 암호가 풀리는 구조라서요.

그래서 "얼마나 빨리 쪼갤 수 있나"는 수학과 암호 양쪽에서 오래된 질문이에요. 속도는 보통 L[α] 형태로 적는데요. α가 1이면 자릿수가 늘 때 시간이 지수적으로 폭발하는 '무식한' 방법, α가 0이면 자릿수의 다항식만큼만 늘어나는 '빠른' 방법이에요. α가 1/2, 1/3로 작아질수록 그 사이에서 빠른 쪽으로 가까워지는 것. 뒤에 붙는 상수(c)는 같은 등급 안에서의 세부 속도예요.

**예전엔 어땠어?**

현실에서 가장 빠른 방법은 일반 수체 체(General Number Field Sieve, GNFS)예요. 1990년대에 나왔고, 속도는 L[1/3], 상수는 약 1.9예요. 문제는 이 속도가 '증명된' 게 아니라는 점이에요. GNFS가 빨리 끝나려면 어떤 다항식의 값들이 작은 소수로만 이루어진 수('매끄러운 수')로 충분히 자주 나와야 하는데, 이게 실험으로는 맞아 보여도 증명은 안 돼 있었어요.

가정 없이 증명된 최고 기록은 1992년 렌스트라(Lenstra)와 포머런스(Pomerance)의 L[1/2]였어요. 정리하면 실제로는 L[1/3]로 돌아가는데 수학적으로 보장할 수 있는 건 L[1/2]까지였던 거예요. 논문은 이 틈이 "30년 넘게" 이어졌다고 썼어요.

**이번엔 뭐가 달라졌어?**

코젠틱 논문은 가정 없이 L[1/3]을 증명했다고 주장해요. 정확한 주장은 이래요. 어떤 정수 N이 들어와도 완전한 소인수분해를 내놓는 확률적 알고리즘이 있고, 틀린 답은 절대 내지 않으며(나온 소수는 AKS 소수 판정으로 확인하고 곱해서 N과 맞춰 봄), 평균 실행 시간이 L[1/3] 등급에 상수 105 이하라는 것.

논문은 GNFS를 증명 불가능하게 만들던 걸림돌을 네 가지로 꼽았어요. 매끄러운 수의 분포를 셀 때 끼어드는 '지겔 영점(Siegel zero)' 문제, 고정된 다항식 값이 매끄럽다는 걸 보장하지 못하는 문제, 대수적 수가 정말 제곱수인지 확인하고 제곱근을 구하는 문제, 그리고 힘들게 찾은 관계식이 결국 쓸모없는 답으로 끝날 수 있는 문제예요. 논문은 다항식을 무작위로 뽑는 방식 등 네 가지 장치로 이걸 한꺼번에 피했다고 설명해요.

같은 날 올라온 짝 논문도 있어요. 동전 던지기 같은 무작위성을 전혀 쓰지 않는 '결정론적' 알고리즘으로 어떤 합성수든 약수 하나를 찾는 데 L[3/4] 수준의 시간이면 된다고 증명했다는 주장이에요. 확률적 방법보다는 느리지만, 오피스차이(OfficeChai)는 완전히 결정론적이면서 완전히 증명된 지수 미만(subexponential) 소인수분해는 이게 처음이라고 전했어요.

**AI는 무엇을 했어?**

논문 각주와 설명에 따르면 이 논문과 Lean 4(컴퓨터가 증명을 한 줄씩 검사하는 언어) 형식화는 제미나이 4(Gemini 4)를 바탕으로 한 코젠틱이 "전적으로" 얻은 것이고, 처음에 증명과 형식화를 요청한 것 말고는 사람의 개입이 없었다고 해요. 코젠틱은 구글 리서치·딥마인드 연구진 7명이 만든 에이전트 틀이고, 9월 arXiv 논문으로 처음 공개됐어요. 같은 저장소에는 11월 18일·23일 날짜로 경매 이론·학습 이론 논문 3편이 먼저 올라 있었어요.

**어디까지 믿어도 돼?**

먼저 암호 이야기는 선을 그어야 해요. 상수 105는 GNFS의 약 1.9보다 훨씬 커요. 논문도 상수를 최적화하지 않고 알아보기 쉬운 값을 골랐다고 밝혔어요. 이 알고리즘으로 실제 RSA 키를 더 빨리 깰 수 있다는 뜻이 아니라, 지금 쓰는 방법의 속도 등급이 수학적으로 정당하다는 걸 보였다는 이론상 결과인 것.

다음은 검증이에요. 논문은 아직 동료 심사를 거치지 않았어요. Lean 형식화는 "완성됐다"고 했지만 공개하지 않았고 후속 제출로 내놓겠다고 했어요. 형식 증명이 공개되면 컴퓨터로 맞는지 확인할 수 있지만, 지금은 논문 본문만 있는 상태예요. 저장소에는 "구글 공식 제품이 아니다"라는 문구도 붙어 있어요. 같은 묶음의 로그-랭크 논문처럼 개선 폭이 지수에서 0.000005에 그치는 결과도 섞여 있어서, 6편의 무게가 모두 같지는 않아요.

※ 이 글은 논문의 주장을 이해를 돕는 수준으로 줄여 설명한 것이에요. L 표기의 정확한 정의와 증명 세부는 원문을 봐야 해요.
