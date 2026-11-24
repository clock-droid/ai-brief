---
title: "싼 AI 추론 업체 3곳서 사용자 키 탈취, 드라고스 조사"
date: 2026-11-24T07:09:00+09:00
category: safety
sources:
  - name: The Decoder
    url: https://the-decoder.com/security-researchers-show-how-cheap-ai-inference-providers-steal-keys-and-snoop-on-users/
    published: 2026-11-22T12:07:56+00:00
figure:
  src: https://the-decoder.com/wp-content/uploads/2026/11/cybersecurity-Openrouter.png
  alt: "오픈라우터가 사용자에게 보낸 메일. MiniMax 모델로 보낸 요청을 제3자가 읽었을 수 있다는 경고와 해당 계정의 요청 건수가 적혀 있음"
  caption: "오픈라우터가 영향받은 사용자에게 보낸 경고 메일. MiniMax 모델로 보낸 요청을 제3자가 읽었을 수 있다고 알림"
  credit: The Decoder
  url: https://the-decoder.com/security-researchers-show-how-cheap-ai-inference-providers-steal-keys-and-snoop-on-users/
  width: 714
  height: 998
---

- 보안업체 드라고스(Dragos)가 7~11월 가짜 자격증명을 넣은 AI 요청 약 200만 건을 보내 추론 중개 서비스를 시험함.
- 공격자가 실제로 사용자 데이터를 훔치고 있는 침해된 업체를 최소 3곳 확인했고, 업체들은 드라고스가 알리기 전까지 침해 사실을 몰랐음.
- 가장 큰 사건에서는 AWS 키 수백 개가 수집됐고, 일부는 몇 시간 안에 시험·S3 저장소 탐색에 쓰였음.
- 중개 업체가 최저가로 모델을 올리고 로깅만 켜도 취약점 없이 고객 요청을 읽을 수 있었고, 데이터 무보관(Zero Data Retention) 설정도 자주 무시됐음.
- 오픈라우터(OpenRouter)는 업체 3곳을 퇴출하고 125개 엔드포인트의 무보관 승인을 철회했다고 밝힘.

한 줄 요약: 값싼 AI 추론 중개 서비스에서 요청 내용과 자격증명이 읽히거나 탈취되는 사례가 확인됨.

※ 드라고스의 조사 결과를 The Decoder가 전한 것이며 독립 검증은 아님. 일부 업체는 아직 보고서를 내지 않음. (원문 드라고스 블로그는 직접 확인하지 못함.)
