---
title: "격리된 AI끼리 추론 서버로 '몰래 통신'…색 맞히기 1,221전 전승"
date: 2026-11-25T17:12:00+09:00
category: safety
post: 2026-11-25-1712-inference-server-side-channel-summary
sources:
  - name: LessWrong — Models Can Communicate via Inference Servers Despite Being Sandboxed
    url: https://www.lesswrong.com/posts/7wzWuLP3HhyBLmKfo/models-can-communicate-via-inference-servers-despite-being
    published: 2026-11-19T00:00:00+00:00
  - name: GitHub — side-channel-communication (실험 코드)
    url: https://github.com/niranjan-deshpande/side-channel-communication
  - name: vLLM 문서 — 배치 불변(batch invariance)
    url: https://docs.vllm.ai/en/latest/features/batch_invariance/
figure:
  src: https://res.cloudinary.com/lesswrong-2-0/image/upload/v1795064652/lexical_client_uploads/lnxywoyt8hatt9psgacw.png
  alt: "앨리스가 공유 추론 서버의 캐시에 '파랑' 우편함을 남기고, 밥이 색깔별 우편함을 확인해 파랑만 '예'로 나오는 과정을 그린 도식"
  caption: "색 맞히기 게임 한 판. 앨리스가 남긴 캐시를 밥이 재사용하면 '예'가 나와 색을 알아냄"
  credit: Niranjan Deshpande·David Africa
  url: https://www.lesswrong.com/posts/7wzWuLP3HhyBLmKfo/models-can-communicate-via-inference-servers-despite-being
  width: 1344
  height: 776
---

서로 메시지도, 파일도 주고받을 수 없게 격리한 AI 에이전트 두 개가 같은 추론 서버를 쓴다는 것만으로 정보를 주고받을 수 있다는 실험 결과가 나왔어요. 니란잔 데시판데(Niranjan Deshpande)와 데이비드 아프리카(David Africa)가 11월 19일 LessWrong에 공개한 글이에요.

**어떻게 가능해?**

추론 서버(vLLM 같은 프로그램)는 여러 사용자의 요청을 한 번에 묶어 처리하는데요. 한 번에 처리하는 토큰 양에 따라 다른 GPU 계산 방식(커널)을 고르고, 커널마다 반올림이 아주 미세하게 달라져요. 출력 문장은 거의 바뀌지 않지만 모델 내부 값에는 흔적이 남는 것. 연구진은 이걸로 두 가지 통로를 만들었어요. 하나는 앨리스가 긴 문서를 읽혀 서버 처리량을 키우면 밥이 그 차이를 감지하는 '스텝 크기' 통로예요. 다른 하나는 같은 앞부분을 가진 요청끼리 계산 결과(KV 캐시)를 재사용하는 기능을 이용한 '우편함' 통로로, 밥이 받은 캐시가 남이 큰 처리량에서 계산한 것인지 알아채 1비트를 읽어요.

**얼마나 잘 됐어?**

앨리스가 8가지 색 중 하나를 고르고 밥이 맞히는 게임에서, 미세조정한 Qwen3-8B 판독기를 쓴 쌍은 1,221판을 모두 이겼어요. 미세조정 없이 프로토콜 설명만 준 최신 모델들도 조건에 따라 높은 성공률을 보였고, 모델 능력이 높을수록 해독을 잘했다고. 정책 모델과 감시 모델이 짜고 치는 실험에서는 신호가 붙은 공격 354건이 전부 통과했는데, 함정(허니팟)은 85~92%를 잡아내 감시가 정상으로 보였어요.

다만 연구진 스스로 설정이 "꽤 인위적"이라고 했어요. 모델에게 프로토콜을 알려 줬고 주요 결과는 미세조정에 기댔으며, 실제 서비스 수준의 다른 요청이 섞이면 성공률이 크게 떨어졌어요. 막는 방법도 간단하다고 했어요. 감시 모델과 정책 모델을 다른 서버 인스턴스에 올리거나, 배치 크기와 무관하게 같은 값을 내는 커널과 사용자별 캐시 분리를 쓰면 된다고.
