---
title: "AI 에이전트가 설계한 CPU '프로스트바이트', 와트당 성능 4.59배 주장"
date: 2026-11-24T03:08:00+09:00
category: infra
sources:
  - name: AI타임스
    url: https://www.aitimes.com/news/articleView.html?idxno=217705
    published: 2026-11-23T08:10:00+00:00
  - name: Xenospectrum
    url: https://xenospectrum.com/en/frostbite-cpu-design-energy-efficiency/
---

- 미국 스타트업 아키텍트랩스(Architect Labs)가 11월 18일 AI 에이전트로 설계한 CPU 아키텍처 '프로스트바이트(Frostbite)'를 공개함. 명령어 체계·회로 설계·검증·배치도 생성을 AI가 맡고, 사람은 성능 목표와 검증 조건을 정했다고 밝힘.
- 프로그램에 들어 있는 병렬 작업을 그대로 쓰는 인터랙션 넷(Interaction Nets, 계산을 노드와 연결로 표현하는 모델) 기반이며, 공유 캐시 대신 처리 장치별 로컬 메모리를 씀.
- 25개 작업 평균으로 면적이 비슷한 기존 순차 실행 CPU 코어보다 와트당 성능 4.59배, 면적당 성능 8.77배 높음. 설계 최적화에 쓰지 않은 15개 작업만 보면 와트당 3.83배임.
- 다만 실제 칩이 아니라 7나노 공정을 가정한 시뮬레이션 결과이고, 비교 대상 CPU 모델은 공개되지 않았음. 원문(아키텍트랩스 블로그)은 확인하지 못했고 AI타임스·Xenospectrum 보도 기준임.

한 줄 요약: AI가 설계했다는 CPU가 시뮬레이션에서 기존 코어보다 와트당 성능 4.59배를 냈다고 회사가 주장함.

※ 비교 대상과 실제 칩 측정값이 없어 제품 성능으로 읽을 수 없음.
