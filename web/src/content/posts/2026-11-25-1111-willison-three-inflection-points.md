---
title: "사이먼 윌리슨: 12개월 동안 LLM이 넘은 변곡점 3개"
date: 2026-11-25T11:11:00+09:00
category: agents
format: 원문 요약
summary:
  - "개발자 사이먼 윌리슨은 지난 1년 동안 LLM 코딩 능력에 변곡점이 세 번 있었다고 정리했다. 2025년 11월 코딩 에이전트, 2026년 6~7월 '페이블급' 모델, 9~10월 3D·게임 개발이다."
  - "페이블급은 목표와 도구만 주면 '무차별 대입(brute force)'으로라도 문제를 풀어 내는 모델이다. 그는 이게 이제 프런티어 모델의 기본값이 됐다고 봤다."
  - "페이블 5.2가 네 번째 변곡점인지는 아직 판단을 미뤘고, 소프트웨어 개발은 1년 새 '알아볼 수 없을 만큼' 바뀌었다고 결론 냈다."
sources:
  - name: Simon Willison — Three LLM inflection points in twelve months
    url: https://simonwillison.net/2026/Nov/24/llm-inflection-points/
    published: 2026-11-24T23:02:07+00:00
figure:
  src: https://static.simonwillison.net/static/2026/fable-class.webp
  alt: "어두운 배경에 흰 글씨로 'Inflection point 2: Fable class models / If you can define a goal and provide necessary tools / They can solve your problem with brute force'라고 적힌 발표 슬라이드"
  caption: "윌리슨 기조연설의 두 번째 변곡점 슬라이드. 목표와 도구만 주면 무차별 대입으로 문제를 푸는 '페이블급' 모델을 정의함"
  credit: Simon Willison
  url: https://simonwillison.net/2026/Nov/24/llm-inflection-points/
  width: 1920
  height: 1080
---

개발자이자 LLM 도구 블로거인 사이먼 윌리슨(Simon Willison)이 11월 24일 블로그에 올린 글이다. 몇 주 전 AI Engineer Code Summit 기조연설을 바탕으로, 그 핵심 주제인 "변곡점"을 더 깊게 따졌다. 원문: simonwillison.net/2026/Nov/24/llm-inflection-points/

**변곡점 1: 코딩 에이전트 (2025년 11월)**
글을 쓴 날은 Claude Opus 4.5 출시 1주년이다. 앤트로픽은 당시 Opus 4.5가 여러 시스템에 걸친 복잡한 버그의 "고칠 방법을 알아낸다"고 했고, 윌리슨은 그 말이 맞았다고 본다. 2025년 2월 나온 Claude Code는 그때 9개월째였는데, Opus 4.5와 함께 쓰면서 처음으로 기본 결과물이 대체로 옳았다는 것이다.

> "Opus 4.5 was the first model I had used with Claude Code where the default result was generally the right thing." (Claude Code에서 써 본 모델 중, 기본으로 나오는 결과가 대체로 맞았던 건 Opus 4.5가 처음이었어요.)

같은 달 OpenAI의 GPT-5.1 계열도 Codex에 비슷한 효과를 냈다. 사람들은 12월 내내 이것저것 시험했고, 1월부터는 실제 업무에 쓰기 시작했다.

**변곡점 2: 페이블급 모델 (2026년 6~7월)**
4월 앤트로픽은 사이버보안 능력이 "너무 위험하다"며 Claude Mythos를 공개하지 않았다. 6월에는 보안 작업을 막은 "이빨 뺀 Mythos" Claude Fable 5가 나왔는데, 사흘 만에 미국 수출 통제로 사실상 내려갔다가 7월 1일 돌아왔다. 윌리슨은 "목표를 정해 주고 필요한 도구를 주면 무차별 대입으로라도 문제를 푸는" 모델을 '페이블급(Fable class)'이라 부른다. 예로 사파리 화면 버그를 잡으려고 스스로 스크린샷 장치와 로컬 로그 서버까지 만든 일, 웹오디오 마이크 5개로 정체불명의 삑 소리 위치를 약 40cm 안으로 찾아낸 일을 든다. 페이블 5·5.1·5.2, Opus 5.5('싼 페이블'), GPT-6 Astra, 어쩌면 Gemini 4 Neon까지 이 부류이고, 이제 이것이 프런티어 모델의 기준선이 됐다고 본다.

**변곡점 3: 3D와 게임 개발 (2026년 9~10월)**
최근 넉 달 사이 프런티어 모델이 블렌더(Blender)나 Three.js로 하는 3D 작업에 강해졌다. 8월만 해도 페이블 5가 만든 3D 게임은 재미가 없었고, 그는 "재미있는 게임 설계는 아직 사람 몫"이라며 안심했다. 그런데 9월 22일 나온 Opus 5.5가 약 12시간의 시험 플레이 끝에 그의 실시간 전략 게임 밸런스를 다시 잡았다. 그는 Opus 5.5를 "재미를 이해하는 것처럼 보인" 첫 모델이라 부른다. 인디 게임계에서는 AI 활용을 두고 격한 논쟁이 벌어지고 있다는 점도 덧붙였다.

**열린 질문: 페이블 5.2**
페이블 5.2가 새 변곡점인지, 점진적 개선인지는 아직 모르겠다고 한다. 다만 취향이 자기와 아주 잘 맞고, 3주 만에 Datasette와 LLM 도구를 여러 번 새로 낼 수 있었다고 했다. 그의 요약은 이렇다. 머릿속에 그릴 수 있고 분명히 설명할 수 있는 소프트웨어라면 페이블이 만들어 낸다.

**결론**
소프트웨어 개발은 1년 만에 "알아볼 수 없을 만큼" 바뀌었고, 코드 대부분을 손으로 치던 시절로 돌아갈 일은 없을 것 같다고 맺는다. 다만 '재미를 이해한다', '싼 페이블' 같은 판단은 자기 프로젝트에서 얻은 주관적 인상이라는 점을 그 스스로도 숨기지 않는다.
