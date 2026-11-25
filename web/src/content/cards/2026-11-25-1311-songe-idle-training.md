---
title: "쉬는 동안 스스로 배우는 로컬 모델 엔진 'Songe' 공개"
date: 2026-11-25T13:11:00+09:00
category: agents
sources:
  - name: GitHub — sous-labs/songe
    url: https://github.com/sous-labs/songe
  - name: GeekNews
    url: https://news.hada.io/topic?id=37798
    published: 2026-11-24T23:31:27+00:00
---

- sous-labs가 로컬 모델을 쓰는 동안 도구 실행 결과·오류·사용자 수정을 기록했다가, 에이전트가 쉴 때 그걸로 모델을 학습시키는 엔진 Songe를 Apache-2.0으로 공개함.
- 'Quick Dream'은 몇 분 안에 사용자 선호를 모델 지침에 넣고, 'Deep Dream'은 1시간 넘게 연습 상황을 만들어 작은 어댑터를 학습함.
- 실제 대화를 그대로 학습하지 않고, 모델이 만든 연습 과제로 온폴리시 증류(on-policy distillation, 학생 모델이 직접 낸 답을 교사가 고쳐 주는 학습)를 함.
- 새 버전은 사용자가 반응했던 지점에서 기존 버전보다 분명히 낫고 잘하던 동작을 유지할 때만 적용되며, 언제든 되돌릴 수 있음.
- 다만 개선 폭을 보여 주는 벤치마크 수치는 공개하지 않음.

한 줄 요약: 데이터를 밖으로 보내지 않고 내 컴퓨터의 놀고 있는 연산으로 로컬 모델을 계속 고쳐 쓰는 오픈소스 도구가 나옴.

※ LM Studio·vLLM·Ollama 등과 붙고, GPU가 없는 기기는 기록만 하고 학습은 못 함.
