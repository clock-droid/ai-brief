---
title: "앤트로픽 내부 Claude 모델, 모든 체에서 VP ≠ VNP 증명 공개"
date: 2026-11-24T09:09:00+09:00
category: science
sources:
  - name: Anthropic formal-math (GitHub)
    url: https://github.com/anthropics/formal-math/tree/main/vp-vnp
    published: 2026-11-23T23:31:40+00:00
---

- 앤트로픽(Anthropic)이 내부 연구용 Claude 모델이 찾아낸 "VP ≠ VNP"(대수적 회로 복잡도 버전의 P vs NP) 결과의 논문과 Lean 4 형식화를 GitHub에 공개함.
- 해밀턴 순환 다항식과, 표수가 2가 아닌 체의 퍼머넌트(permanent)를 계산하는 회로에는 충분히 큰 m에서 m^(c (log m)^(1/3)) 개보다 많은 게이트가 필요하다고 주장함.
- 근사 회로에도 같은 하한이 적용되어, VP는 VNP의 진부분집합이고 VNP는 VP의 폐포에도 들지 않는다는 결론임.
- 논문과 Lean 코드 모두 AI 모델이 작성했고, 인간 수학자는 아직 증명을 검토하지 않았다고 저장소가 밝힘.
- 다만 Lean은 증명만 검사하며, 형식화된 명제가 논문 주장과 일치하는지는 기계가 확인하지 않음. 논문 부록 Q가 대응표와 차이를 정리함.

한 줄 요약: AI가 쓴 논문과 Lean 증명이 공개됐고, 전문가 검토는 아직 없음.

※ 대수적 회로 모델의 결과이며, 원래의 P vs NP는 풀지 못했다고 저장소가 명시함.
