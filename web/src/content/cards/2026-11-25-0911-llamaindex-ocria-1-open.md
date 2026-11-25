---
title: "라마인덱스 문서 OCR 4B 모델 OCRia-1 가중치 공개"
date: 2026-11-25T09:11:00+09:00
category: models
sources:
  - name: X (@jerryjliu0)
    url: https://x.com/jerryjliu0/status/2125266115874144473
  - name: Hugging Face — llamaindex/OCRia-1
    url: https://huggingface.co/llamaindex/OCRia-1
    published: 2026-11-24T16:31:42+00:00
tweet:
  author: Jerry Liu
  handle: jerryjliu0
  text: "Today we are open-sourcing the weights to OCRia-1, our flagship 4B VLM for document OCR 🔥 This is our SECOND open-weight release in two days (we just launched OCRia-nano-1 yesterday!!). OCRia-1 is on the pareto curve of accuracy and cost relative to other 4B models on multiple… pic.twitter.com/Nsi5bxFRtK"
  url: https://x.com/jerryjliu0/status/2125266115874144473
---

- 라마인덱스(LlamaIndex) CEO 제리 류(Jerry Liu)가 문서 판독용 40억(4B) 파라미터 시각언어모델 OCRia-1의 가중치를 11월 24일 공개함. 전날 OCRia-nano-1에 이은 이틀 새 두 번째 공개임.
- 페이지 이미지를 받아 마크다운으로 쓰고, 표는 HTML로, 차트는 데이터 표로, 수식은 LaTeX로 바꿈. 별도 레이아웃 검출기나 OCR 엔진 없이 한 번 호출로 처리함.
- 문서 판독 벤치마크 ParseBench 2에서 85.2점(61개 시스템 중 7위), ParseBench 1에서 84.7점(158개 중 2위)으로 공개 가중치 모델 중 1위라고 함. 차트 항목은 82.5점으로 다음 공개 모델(69.1점)보다 13.4점 높음.
- 기반 모델은 큐원3.5-4B(Qwen3.5-4B)이고, 자체 라이선스로 배포됨.

한 줄 요약: 표·차트·수식이 많은 문서를 마크다운으로 옮기는 4B 모델이 공개 가중치로 풀림.
