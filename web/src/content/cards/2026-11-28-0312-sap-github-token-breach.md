---
title: "SAP, 보안 사고 확인…\"직원 토큰으로 깃허브 코드 복사·변조\" 보도"
date: 2026-11-28T03:12:00+09:00
category: tech
sources:
  - name: Techmeme — SecurityWeek 보도 요약
    url: https://www.techmeme.com/261127/p9#a261127p9
    published: 2026-11-27T16:35:08+00:00
  - name: The Next Web — SAP confirms security incident after reported GitHub breach
    url: https://thenextweb.com/news/sap-security-incident-github-breach
    published: 2026-11-27T12:41:00+00:00
---

독일 소프트웨어 기업 SAP가 11월 26일(현지 목요일) 저녁 보안 사고가 있었다고 인정했어요. 회사는 "수상한 활동을 발견해 필요한 조치를 바로 했다"며, 지금까지 고객 업무 데이터에 누가 접근한 흔적은 없다고 밝혔어요. 무슨 활동이었는지, 언제 발견했는지는 말하지 않았어요.

자세한 내용은 독일 슈피겔(Der Spiegel) 보도에서 나왔어요. 내부 소식통에 따르면 공격자가 SAP 직원들의 접속 토큰(로그인을 대신하는 인증 열쇠)을 훔쳐 깃허브(GitHub)에 있던 SAP 소스 코드를 복사하고 고쳤다고 해요. 공격자가 스스로 작업을 이어 가는 AI 에이전트를 썼을 수 있다는 말도 나왔고, 회사 안에선 '프로젝트 그래닛(Project Granite)'이라는 이름의 진행 중 사고로 다룬다고. SAP는 토큰 탈취와 코드 변조 모두 확인하지 않았어요.

SAP는 지난 4월에도 npm(자바스크립트 패키지 저장소)에 올린 자사 패키지 4개가 탈취돼 비밀번호·키를 훔치는 악성코드를 퍼뜨린 적이 있어요. 같은 날 독일 연방정보보안청(BSI)은 자율 AI 공격 도구에 대한 공개 경고를 냈다고 The Next Web은 전했어요. 다만 원문(SecurityWeek·슈피겔)은 직접 확인하지 못했고 The Next Web 보도와 Techmeme 헤드라인 기준이에요.
