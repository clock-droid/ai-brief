---
title: "공개 벤치 점수로 오픈AI 퍼플렉시티 예측…오차 0.016"
date: 2026-11-26T01:12:00+09:00
category: models
sources:
  - name: X (@DimitrisPapail)
    url: https://x.com/DimitrisPapail/status/2125477486318272921
    published: 2026-11-25T06:31:36+00:00
  - name: GitHub — microsoft/benchpress
    url: https://github.com/microsoft/benchpress
  - name: arXiv — You Don't Need to Run Every Eval (BenchPress 논문)
    url: https://arxiv.org/pdf/2606.24020
  - name: OpenAI — Perplexity and Intelligence (배경)
    url: https://openai.com/index/perplexity-and-intelligence
    published: 2026-11-22T00:00:00+00:00
tweet:
  author: Dimitris Papailiopoulos
  handle: DimitrisPapail
  text: "in case you were wondering what the predicted log-perplexity is of all non openai models https://t.co/sBczP5JWfW pic.twitter.com/x73zjOkHKR"
  url: https://x.com/DimitrisPapail/status/2125477785049198661
post: 2026-11-24-1111-pachocki-perplexity-intelligence
---

오픈AI(OpenAI)가 공개한 모델별 로그 퍼플렉시티를 공개 벤치마크 점수만으로 거의 맞힐 수 있다는 분석이 나왔어요. 마이크로소프트 리서치(Microsoft Research)의 디미트리스 파파일리오풀로스(Dimitris Papailiopoulos)가 11월 25일 X에 올린 결과인데, 한 모델씩 빼고 예측했을 때 평균 오차가 0.016이었다고 해요. 그는 같은 방법으로 앤트로픽·구글·딥시크 등 다른 회사 모델의 값도 추정해 그래프로 공개했어요.

**로그 퍼플렉시티가 왜 화제야?**

로그 퍼플렉시티는 모델이 다음 단어를 얼마나 헷갈려하는지 나타내는 값으로, 낮을수록 예측을 잘한다는 뜻이에요. 오픈AI 수석 과학자 야쿠프 파호츠키(Jakub Pachocki)는 11월 22일 "퍼플렉시티와 지능" 글에서 내부 코드 데이터셋 기준 수치를 처음 공개했는데요. GPT-3.5가 약 0.99, GPT-4가 약 0.91이었고, 0.8 아래에서 사이버보안·수학 능력이 나타났다고 했어요. 그런데 다른 회사들은 이 값을 공개하지 않아서, 오픈AI 모델과 같은 잣대로 비교할 방법이 없었던 것.

**어떻게 예측했어?**

쓰인 도구는 파파일리오풀로스와 유천 정(Yuchen Zeng)이 6월에 낸 벤치프레스(BenchPress)예요. 84개 모델 × 133개 벤치마크 점수표를 모아 보니 빈칸이 77%나 되는데도 두 개의 요인만으로 분산의 90% 이상이 설명됐다고 해요(낮은 차원 행렬 완성, rank-2 matrix completion). 비어 있는 칸을 나머지 점수로 메우는 방식이라, 퍼플렉시티를 하나의 '열'로 넣으면 공개 점수에서 그 값을 추정할 수 있는 셈이에요. 그래프상 오픈AI 13개 시점의 예측 순위 상관(스피어먼)은 0.96이었어요.

**어디까지 믿어도 돼?**

그래프에 적힌 대로 다른 회사 값은 "측정이 아니라 오픈AI 기준으로 환산한 추정치"예요. 기준이 된 오픈AI 수치도 블로그 그래프에서 눈으로 읽은 값이고, 학습에 쓴 점은 13개뿐이에요. 다른 회사 모델은 데이터 구성도 다르니, 같은 퍼플렉시티라도 같은 능력을 뜻한다는 보장은 아직 없어요.
