---
title: "샘소나이트 등 쇼핑몰 5곳, 결제창에 카드 탈취 코드"
date: 2026-11-28T07:12:00+09:00
category: tech
sources:
  - name: InfoHawk — Black Friday WebRTC skimmer
    url: https://www.infohawk.com/news/2026-11-27-black-friday-webrtc-skimmer
    published: 2026-11-27T00:00:00+00:00
  - name: GeekNews — 인기 쇼핑 사이트에서 WebRTC를 이용한 신용카드 정보 탈취 스크립트 발견
    url: https://news.hada.io/topic?id=37967
    published: 2026-11-27T19:35:50+00:00
---

블랙프라이데이 직전, 샘소나이트(Samsonite)·아메리칸 투어리스터(American Tourister)·라스카나(Lascana)·리볼브(Revolve)·FWRD 온라인 매장 결제 페이지에서 카드 정보를 빼내는 코드가 발견됐다고 보안 매체 인포호크(InfoHawk)가 11월 27일 전했어요. 신고 뒤 24~25일 모두 제거됐어요.

눈에 띄는 건 통로예요. 보통 이런 '스키머'는 일반 웹 요청으로 정보를 내보내 보안 도구에 걸리기 쉬운데요. 이번 코드는 화상통화용 기술인 WebRTC의 데이터 채널로 악성 코드를 받아 오고 카드 번호·유효기간·보안코드·주소까지 내보냈다고. 웹사이트가 허용된 곳과만 통신하게 막는 보안 정책(CSP)도 이 채널은 막지 못한다고 해요. 쿠키 배너·마케팅 픽셀 같은 제3자 스크립트를 타고 들어왔고, 휴대폰처럼 작은 화면에서만 작동해 데스크톱 점검으로는 놓치기 쉬웠다고.

다만 실제로 정보가 빠져나가는 게 확인된 건 라스카나의 시험용 카드뿐이고, 실제 고객 피해 여부와 규모는 확인되지 않았어요.
