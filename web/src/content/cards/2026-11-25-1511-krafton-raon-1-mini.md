---
title: "크래프톤, 처음부터 학습한 29B 오픈 모델 'Raon-1 mini' 공개"
date: 2026-11-25T15:11:00+09:00
category: models
sources:
  - name: Hugging Face — KRAFTON/Raon-1-mini
    url: https://huggingface.co/KRAFTON/Raon-1-mini
    published: 2026-11-24T13:17:11+00:00
  - name: 디일렉 — 삼성전자, 내년 초 CXL 3.2 샘플 공급 (KV 캐시 설명)
    url: https://www.thelec.kr/news/articleView.html?idxno=65894
    published: 2026-11-25T05:02:59+00:00
---

게임사 크래프톤(KRAFTON)의 AI 조직이 처음부터 직접 학습한 언어 모델 Raon-1 mini를 허깅페이스에 Apache 2.0으로 공개했어요. 한국어 대화와 에이전트 작업에 맞춘 모델로, 공개 하루 만에 허깅페이스 급상승 목록에 올랐어요.

**어떤 모델이야?**

전체 288억(28.8B) 개 파라미터 가운데 단어 하나를 처리할 때 43억(4.3B) 개만 쓰는 전문가 혼합(MoE, Mixture of Experts) 구조예요. 128개의 '전문가' 묶음 중 필요한 6개와 공용 1개만 골라 쓰는 방식이라, 덩치에 비해 계산은 가벼운 것. 25개 층 가운데 18개는 크래프톤이 'Raon Delta Attention'이라 부르는 선형 어텐션(linear attention) 층이고, 7개만 일반 어텐션이에요. 대화 맥락을 기억해 두는 KV 캐시를 일반 어텐션 층만 쓰기 때문에 토큰당 약 8KiB로 작다고. 한 번에 읽는 길이는 26만 2,144토큰이에요.

추론 강도를 'none'부터 'max'까지 여섯 단계로 고를 수 있고, 4비트(NVFP4) 양자화판은 RTX 5090 한 장(32GB)에서 돌아간다고 밝혔어요.

**성능은 어디쯤이야?**

크래프톤이 비슷한 크기의 MoE 모델과 비교한 표를 보면 강점과 약점이 갈려요.

- 한국어 대화(자체 평가) 92.7점으로 비교 대상 중 가장 높아요. 큐원(Qwen)3.6-35B-A3B는 74.5점, 젬마(Gemma) 4 26B-A4B는 90.6점이에요.
- 웹 검색 과제 BrowseComp Plus는 55.9점으로 큐원3.6(34.8점)보다 21점 넘게 앞서요.
- 반면 터미널 작업(Terminal-Bench Lite)은 52.0점으로 큐원3.6(63.3점)보다 낮고, 코딩(SWE-Verified)은 71.0점으로 플린트(Flint) 40B-A2.5B(76.0점)에 뒤져요.

다만 이 점수는 모두 크래프톤이 직접 정한 채점 방식과 설정으로 잰 것이고, 외부 기관의 측정은 아직 없어요.
