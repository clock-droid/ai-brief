---
title: "카파시, 클로드로 7시간 만에 '문명'식 미국 지도…코드 4.5만 줄"
date: 2026-11-28T01:12:00+09:00
category: agents
tweet:
  author: Andrej Karpathy
  handle: karpathy
  text: "I asked Claude to populate a Civilization-style game map with real data from the US. Opus 5.5 downloaded and parse a ton of public data and 7 hours and 45K lines of code later... it works :) - 31 real data sources including Census, BEA, BLS, EIA, NOAA, USGS, DoD, NPS, FAA, FEMA,… pic.twitter.com/HiXfcCLxeO"
  url: https://x.com/karpathy/status/2125779541952246039
sources:
  - name: X (@karpathy)
    url: https://x.com/karpathy/status/2125779541952246039
  - name: usaciv (데모)
    url: https://karpathy.ai/usaciv/
  - name: Digg — Karpathy says Claude built a Civilization-style U.S. map
    url: https://digg.com/ai/7at6677g
  - name: 유튜브 — Datapizza
    url: https://www.youtube.com/watch?v=Nxs3uZiRMfo
    published: 2026-11-26T19:00:31+00:00
---

안드레이 카파시(Andrej Karpathy)가 11월 26일 X에, 클로드 오퍼스 5.5(Claude Opus 5.5)에게 미국 실제 데이터로 게임 '문명(Civilization)' 같은 지도를 채우게 했더니 7시간, 코드 4만 5,000줄 끝에 "돌아간다"고 밝혔어요. OpenAI 공동 창업자로, 지금은 앤트로픽에서 일하는 사람이에요. 결과물은 karpathy.ai/usaciv에 공개돼 있어요.

AI가 직접 인구조사국(Census)·노동통계국(BLS)·에너지정보청(EIA)·해양대기청(NOAA)·지질조사국(USGS)·국방부 등 공공 데이터 31종을 내려받아, 고도·땅 쓰임·GDP·일자리·발전소·항구·공항·국립공원·대학·화물 흐름·재난을 한 변 25km짜리 육각형 칸 위에 맞췄다고 해요. 게임 규칙도 데이터에서 나왔는데요. 도시가 만드는 금은 실제 GDP이고, 산호세엔 '캠퍼스', 디트로이트엔 '모터 시티'처럼 실제 주력 산업이 구역이 되는 식이에요. 산호세 노동자 4명 중 1명이 엔지니어·개발자·과학자(전국은 14명 중 1명)라는 것도 시민 구성에 반영됐다고. 소득·학력·재난 등 19개 보기, 대도시권 524곳의 도시 화면, 3,100개 넘는 카운티 데이터를 표·산점도로 바꾸는 탐색 도구도 붙었어요.

설정은 클로드 코드 데스크톱 앱에서 오퍼스 5.5 '중간' 노력에 '울트라코드'를 켠 것이었고, 끝나고도 주간 사용량이 절반 남았다고 해요. 다만 카파시 스스로 "클로드가 몇몇 주와 영토는 건너뛰기로 했다"고 적었고, 데이터 정확도나 사람이 얼마나 손댔는지는 그의 설명 말고는 검증되지 않았어요. 이걸 실제 게임으로 키울지도 정하지 않았다고 했어요.
