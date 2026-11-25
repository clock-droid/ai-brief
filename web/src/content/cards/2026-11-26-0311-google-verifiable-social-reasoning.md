---
title: "구글 \"AI 비서, 사용자 말만 듣고 남의 속마음 오판\""
date: 2026-11-26T03:11:00+09:00
category: models
sources:
  - name: Google Research — Verifiable Social Reasoning for LLM Assistants
    url: https://research.google/blog/verifiable-social-reasoning-for-llm-assistants/
    published: 2026-11-25T17:10:27+00:00
figure:
  src: https://storage.googleapis.com/gweb-research2023-media/images/VerifiableSocialReasoning2-HarshAdviceExample.width-1250.png
  alt: "사용자가 새 동료가 금방 동의하고 도와주겠다고 한 게 자기 입지를 깎으려는 거냐고 묻자, 시험 대상 모델이 '너무 착하게 굴지 말라'고 답하는 채팅 화면. 실제 동료는 매우 협조적이었다는 주석이 붙어 있음"
  caption: "실제로는 협조적인 동료를 의심하는 사용자에게 모델이 가혹한 조언을 하는 예"
  credit: Google Research
  url: https://research.google/blog/verifiable-social-reasoning-for-llm-assistants/
  width: 1250
  height: 828
---

구글 리서치(Google Research)가 11월 25일, AI 비서가 사람 관계 고민을 상담할 때 얼마나 정확히 판단하는지 '정답을 확인할 수 있게' 재는 평가 틀을 공개했어요. 모델 12개를 시험한 결론은, 상황을 직접 본 관찰자로서는 잘 맞히던 모델도 사용자 이야기만 전해 들으면 정확도가 크게 떨어진다는 것.

**왜 재기 어려웠어?**

AI 비서는 사용자가 들려주는 이야기로만 상황을 알아요. 그 이야기는 빠진 게 있거나 치우쳐 있을 수 있는데요. 게다가 "그 동료가 왜 그랬는지" 같은 속마음은 원래 정답이 없어서, 기존 평가는 정답을 매기기 쉬운 극단적인 사례 위주였어요.

**어떻게 정답을 만들었어?**

연구진은 오픈소스 다중 에이전트 시뮬레이션 도구 콘코르디아(Concordia)를 확장해 가상의 사회 상황을 돌렸어요. 등장인물 중 한 명에게 숨은 동기(예: 연애 감정인지 우정인지)를 정해 두고 몇 장면에 걸쳐 행동하게 한 뒤, 사용자 역 에이전트가 그 일을 AI 비서에게 부분적·주관적으로 털어놓게 하는 방식이에요. 비서가 숨은 동기를 맞혔는지는 다른 모델이 채점해요. 사용자를 자신만만하게 또는 불안하게 바꿔 가며 시험할 수 있고, 2만 건 넘는 예시 데이터와 틀을 함께 공개했어요.

**결과는?**

사용자가 노골적인 편견을 드러내면 차이가 더 커졌어요. 모델이 근거 없는 의심까지 그대로 받아들이곤 했다는 것. 이야기가 자세할수록 정확도는 올랐지만, 대화를 길게 이어 간다고 나아지지는 않았어요. 연구진 표현으로 "긴 대화가 사회적 추론 정확도를 늘 높이지는 않는다"고 하는데요. 앞선 대화에 고정돼 사용자의 틀을 더 굳히는 경향이 있었다고.

다만 블로그에는 모델별 점수가 공개되지 않았고, 짧은 일상 상황만 다뤘으며 채점도 AI가 맡아 실제 사람 관계와 다를 수 있어요.
