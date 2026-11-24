---
title: "오픈AI·시스코, 패치 전 리눅스 보호 오픈소스 'Shirudo' 공개"
date: 2026-11-24T09:09:00+09:00
category: infra
sources:
  - name: OpenAI
    url: https://openai.com/index/introducing-shirudo
    published: 2026-11-23T21:20:00+00:00
figure:
  src: https://images.ctfassets.net/kftzwdyauwt9/bScTLq9smNJq5XAlaHIQW/fab0e70b1aab8ca8dffb70a747056fd7/guardian-agent-desktop-light.png?w=1920&q=80&fm=webp
  alt: "가디언 에이전트가 eBPF 계측으로 커널·네트워크를 관찰하고, eBPF 제어로 취약한 동작을 막는 흐름도"
  caption: "에이전트가 eBPF로 실행 중인 시스템을 관찰하고, 필요한 차단 규칙을 그때그때 만들어 적용하는 구조"
  credit: OpenAI
  url: https://openai.com/index/introducing-shirudo
  width: 1200
  height: 728
---

- 오픈AI와 시스코(Cisco)가 패치를 적용하기 전까지 실행 중인 리눅스 시스템을 보호하는 오픈소스 런타임 Shirudo(일본어로 "방패")를 11월 23일 공개함.
- eBPF(커널 안에서 작은 프로그램을 실행하는 리눅스 기술)로 취약한 코드 경로를 막는 "실드"를 만들고, 재시작 없이 적용함.
- 통제된 시험에서 Codex가 만든 실드가 실행 중인 Elasticsearch에 대한 Java4Shell 공격 시도를 재시작 없이 차단함.
- 실드는 서명·검증 후 로드되고, 운영자가 승인해야 배포됨. 적용 전에 영향을 미리 모니터링할 수 있음.
- 다만 시험은 통제된 환경의 단일 사례임.

한 줄 요약: AI 에이전트가 취약점 방어용 실드를 만들고 운영자가 승인해 배포하는 오픈소스 도구가 나옴.
