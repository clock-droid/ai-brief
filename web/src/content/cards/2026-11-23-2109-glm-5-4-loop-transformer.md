---
title: "지푸 GLM-5.4: 7500억 매개변수로 2~3조급 성능 주장"
date: 2026-11-23T21:09:00+09:00
category: models
sources:
  - name: Z.ai
    url: https://x.com/Zai_org/status/2124805514722771349
    published: 2026-11-23T09:30:00+00:00
  - name: The Next Web
    url: https://thenextweb.com/news/zai-glm-5-4-loop-transformer-coding-model
    published: 2026-11-23T12:00:00+00:00
  - name: Techmeme
    url: https://www.techmeme.com/261123/p11#a261123p11
    published: 2026-11-23T10:50:12+00:00
---

- Z.ai가 GLM-5.4를 공개함. 첫 루프 트랜스포머(Loop Transformer, 같은 층을 반복 통과시키는 구조) 기반 플래그십임.
- GLM-5 기반 모델의 28개 층을 두 번 돌려 매개변수를 늘리지 않고 깊이만 더함. 규모는 약 7500억 매개변수이고, 2조~3조 매개변수 모델급이라고 주장함.
- 30B 모델 실험에서 루프 학습에 드는 연산은 약 10% 늘었고, GPQA-Diamond·MMLU-Pro 평균 출력 길이는 10~14% 줄었다고 밝힘.
- 지금은 GLM 코딩 플랜 구독자만 쓸 수 있음. API는 안전성 평가 뒤, 오픈 웨이트는 안전 보강 뒤 공개한다고 함.
- 다만 GLM-5.4 자체의 벤치마크 점수는 공개되지 않았고, 과도하게 길게 생각하는 문제도 인정함. 원문 블로그는 직접 열지 못했고 The Next Web 보도·Techmeme 요약 기준임.

한 줄 요약: GLM-5.4는 층 반복으로 깊이를 키운 7500억 모델이며, 2~3조급이라는 성능 주장은 아직 검증할 벤치마크가 없음.
