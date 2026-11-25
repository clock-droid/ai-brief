---
title: "애런슨 \"P≠NP 증명, 처음으로 멀지 않다고 느껴\""
date: 2026-11-26T05:12:00+09:00
category: science
sources:
  - name: Shtetl-Optimized (Scott Aaronson) — HOLY SHIT HOLY SHIT HOLY SHIT HOLY SHIT
    url: https://scottaaronson.blog/?p=10379
    published: 2026-11-25T19:01:13+00:00
  - name: OpenAI Math — The logarithmic exponent of finite Fourier transforms (논문)
    url: https://github.com/openai/math/blob/main/preprints/The-logarithmic-exponent-of-finite-Fourier-transforms-November-24-2026/paper.pdf
  - name: arXiv — Two messages suffice for quantum interactive proof systems (Yupan Liu)
    url: https://arxiv.org/abs/2611.31236
    published: 2026-11-23T18:59:31+00:00
post: 2026-11-26-0512-aaronson-holy-shit-summary
---

복잡도 이론가 스콧 애런슨(Scott Aaronson)이 11월 25일 블로그에 "뼛속까지, 처음으로 P≠NP 증명이 멀지 않았다고 느낀다"고 썼어요. 하루 전 글에서 지금 벌어지는 일의 크기를 제대로 전하지 못했다며 다시 쓴 글이고, 제목부터 같은 감탄을 네 번 반복했어요.

**무엇을 보고 이렇게 말했어?**

애런슨은 24일 저녁 동료들과 식사하며 앤트로픽·OpenAI의 VP≠VNP 증명을 소화하던 중, OpenAI가 행렬 곱셈 지수 ω가 정확히 9/4라는 하한 증명을 내놓는 걸 봤다고 했어요. 그가 놀란 지점은 두 가지예요. 답이 무리수가 아닌 깔끔한 분수라는 것, 그리고 "ω가 2보다 크다"는 증명이 P≠NP보다 이렇게 쉬울 줄 몰랐다는 것. 디저트 무렵엔 유한 푸리에 변환에 필요한 선형 게이트 수가 N(log N)^(1/2+o(1))라는 OpenAI 논문도 나왔다고 했어요. 교과서의 고속 푸리에 변환(FFT)은 N log N 단계가 드는데요. 그보다 적게 되는 길과, 더는 줄일 수 없다는 하한을 함께 냈다는 것. 여기에 유판 류(Yupan Liu)가 23일 arXiv에 올린 'QIP(2)=PSPACE' 증명도 더했어요.

**어디까지 믿어도 돼?**

애런슨은 Lean 형식 검증을 근거로 이 결과들을 부정하지 말라고 하면서, OpenAI나 앤트로픽에서 직접 나온 증명은 반대 증거가 없는 한 맞다고 보겠다고 했어요. 다만 이건 개인의 판단이고, 이 논문들의 사람 전문가 검토는 아직 진행 중이에요. 암호를 깨는 결과를 연구소들이 쥐고 있다는 "믿을 만한 신호"가 있다고도 했지만, 검증된 내용이 없어 소문을 퍼뜨리지 않겠다고 선을 그었어요.
