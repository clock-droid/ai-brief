---
title: "구글, AI 에이전트는 지메일·드라이브에 '자사 MCP로만'"
date: 2026-11-27T11:14:00+09:00
category: agents
sources:
  - name: Google Workspace — AI Tools Addendum
    url: https://workspace.google.com/terms/ai-tools
    published: 2026-11-24T00:00:00+00:00
  - name: Tech Stackups — Google's new rules for AI agents on Workspace
    url: https://techstackups.com/articles/google-workspace-ai-agents-mcp/
  - name: GeekNews — Google, AI 에이전트의 Workspace 접근에 자사 MCP 의무화
    url: https://news.hada.io/topic?id=37919
    published: 2026-11-26T21:39:40+00:00
  - name: AI타임스 — 구글, 외부 AI 에이전트에 지메일·드라이브 이용료 부과
    url: https://www.aitimes.com/news/articleView.html?idxno=217820
    published: 2026-11-26T07:04:49+00:00
---

구글이 AI 에이전트가 지메일·드라이브 같은 워크스페이스(Workspace) 데이터에 들어오는 길을 자사 'MCP 서버'로 좁혔어요. 11월 24일 개발자 약관에 붙인 'AI 도구 부속 약관(AI Tools Addendum)'에서, AI 에이전트이거나 AI가 움직이는 도구는 "구글 MCP를 써야 한다"고 못 박은 것. 기술 분석 매체 테크스택업스(Tech Stackups)는 이 요건이 2027년 2월 1일부터 적용된다고 정리했어요.

**MCP가 뭐야?**

MCP(Model Context Protocol)는 AI 에이전트가 메일·문서·일정 같은 외부 서비스에 접속할 때 쓰는 공통 연결 규격이에요. 전원 콘센트 모양을 하나로 맞춘 것에 가까운 것. 예전엔 에이전트 개발사가 지메일 REST API를 직접 불러 메일을 읽고 보낼 수 있었는데요, 이제 AI 에이전트는 구글이 운영하는 MCP 서버(같은 날 8종 공개)나 워크스페이스 CLI를 거쳐야 해요. 에이전트가 아닌 척 분류를 피하는 것도 금지했어요.

**무엇이 막히나?**

테크스택업스에 따르면 공개된 지메일 MCP 서버는 검색·읽기·초안 만들기는 되지만 메일 보내기·답장·전달·초안 수정은 '파트너 전용'이에요. 일반 개발자는 같은 권한을 받아도 메일을 보낼 수 없고, 빈자리를 REST로 메우면 약관 위반이 되는 것. 약관 본문은 사용자 데이터를 "진행 중인, 사용자가 승인한 작업"에만 쓰게 했고, 접근 과정에서 만든 기술 정보(테크스택업스는 임베딩·메모리 색인 등이 해당한다고 봤어요)는 30일 넘게 보관할 수 없으며, 모델 학습·미세조정·증류에 쓰는 것도 금지했어요. 무료 표준(Standard) 등급은 제품별·프로젝트당 하루 MCP 요청 5,000회인데, 지메일 스레드 검색은 1회에 10회로 계산돼 검색만 하면 하루 약 500번이라고.

구글은 유효한 로그인 토큰만으로는 사용자 의도를 보장할 수 없어 정책 점검과 사람 확인을 요청 경로에 둬야 한다고 설명했어요. 반면 테크스택업스는 구글이 경쟁 에이전트의 기능과 워크스페이스 데이터 이용까지 통제하게 된다는 비판도 함께 전했어요. 확장(Scaled) 등급의 요청당 가격과 파트너 자격 기준은 아직 공개되지 않았어요.
