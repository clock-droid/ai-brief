---
title: "양자 대화형 증명, 메시지 2번이면 충분…\"QIP(2)=PSPACE\""
date: 2026-11-26T05:12:00+09:00
category: science
sources:
  - name: arXiv — Two messages suffice for quantum interactive proof systems (Yupan Liu)
    url: https://arxiv.org/abs/2611.31236
    published: 2026-11-23T18:59:31+00:00
  - name: Shtetl-Optimized (Scott Aaronson)
    url: https://scottaaronson.blog/?p=10379
    published: 2026-11-25T19:01:13+00:00
  - name: arXiv — Two-message quantum interactive proofs are in PSPACE (Jain·Upadhyay·Watrous, 배경)
    url: https://arxiv.org/abs/0905.1300
post: 2026-11-25-1111-ai-math-breakthroughs-month
---

양자 컴퓨터를 쓰는 '대화형 증명'은 메시지를 딱 두 번만 주고받아도 가장 강한 형태와 힘이 같다는 증명이 나왔어요. 유판 류(Yupan Liu)가 11월 23일 arXiv에 올린 17쪽 논문으로, 복잡도 이론에서 15년 넘게 열려 있던 질문을 닫았다고 주장해요. 아직 동료 검토 전 원고예요.

**대화형 증명이 뭐야?**

계산 능력이 약한 '검증자'가 능력이 무한한 '증명자'와 메시지를 주고받으며, 증명자의 주장이 맞는지 높은 확률로 가려내는 방식이에요. 시험관이 질문을 몇 번 던져 상대가 정말 답을 아는지 확인하는 것과 비슷하죠. 이렇게 검증할 수 있는 문제의 범위가 메모리를 다항식만큼 써서 풀 수 있는 문제 전체(PSPACE)와 같다는 게 고전 컴퓨터에서도, 양자 컴퓨터에서도(QIP=PSPACE) 이미 알려져 있었어요.

**이번엔 뭐가 달라졌어?**

예전엔 양자 대화형 증명을 메시지 3번까지 줄일 수 있다는 것(키타예프·와트러스, 2000년)과, 2번짜리 QIP(2)는 PSPACE 안에 들어간다는 것(2009년)까지만 알려져 있었어요. 2009년 논문도 이 둘이 같은지는 열린 문제로 남겼고요. 류는 검증자가 얽힌 입자 쌍(EPR 쌍)의 반쪽을 보내고, 증명자의 답 하나만 받아 확인하는 2번짜리 방식으로 PSPACE 전체를 검증할 수 있음을 보였다고 해요. 그래서 QIP(2)=QIP=PSPACE가 된다는 것.

스콧 애런슨(Scott Aaronson)은 블로그에서 이 결과를 소개하며 류가 AI의 도움을 받았고, 그게 너무 일상적이라 아무도 눈썹 하나 까딱하지 않았다고 전했어요. 다만 논문 자체에는 AI 사용에 대한 언급이 없어요.
