---
title: "inclusionAI, 124B 오픈웨이트 Ling-3.2-air 공개…Terminal-Bench 0→27%"
date: 2026-11-24T03:08:00+09:00
category: models
sources:
  - name: 허깅페이스 — inclusionAI/Ling-3.2-air
    url: https://huggingface.co/inclusionAI/Ling-3.2-air
    published: 2026-11-23T03:55:12+00:00
---

- inclusionAI가 오픈웨이트(가중치 공개) 모델 Ling-3.2-air를 허깅페이스에 올림. 라이선스는 MIT임.
- 전체 124B(1,240억) 파라미터 중 토큰당 5.5B만 쓰는 하이브리드 선형 MoE(전문가 혼합) 구조임. 전문가 512개 중 8개를 활성화하고, 이미지·비디오 입력을 받는 네이티브 멀티모달임.
- 전작 대비 AutomationBench-AA 15.7% → 61%, Terminal-Bench 4.0 통과율 0% → 27%, AA-Briefcase v1.1 Elo 987 → 1340(+353)으로 오름. Artificial Analysis Intelligence Index v5.0.1은 23점임.
- 다만 수치는 모두 모델 카드에 제시된 자체 보고이고, 법률 평가 Harvey LAB-AA의 전체 통과율은 환각 검사 후 0.8%로 낮음.

한 줄 요약: 5.5B만 활성화하는 MIT 라이선스 124B 모델이 업무 자동화·터미널 과제 점수를 전작보다 크게 올렸다고 모델 카드에 적힘.
