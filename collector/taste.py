"""취향 점수의 핵심: 반응이 붙은 글(라벨)과 새 후보의 '내용이 얼마나 닮았나'로 점수를 낸다.

이 파일은 이 프로젝트의 파일 위치·글 형식을 모른다. 라벨(글 텍스트 + 좋고 싫은 정도)과 후보 텍스트만 받는다.
다른 곳에 옮길 때는 이 파일을 그대로 쓰고, 라벨을 만드는 부분(이 프로젝트에서는 preferences.py)만 새로 짠다.

방법 (넷플릭스·메타 추천의 '내용 기반' 부분을 한 사람용으로):
1. 다국어 문장 임베딩으로 글을 벡터로 바꾼다 (한국어 카드 ↔ 영어 원문 후보도 같은 공간에서 비교된다).
2. 후보와 라벨 글의 코사인 유사도 s(라벨 글이 여러 판이면 가장 높은 값)가 S_MIN을 넘는 만큼만 '닮음' k = (s - S_MIN) / (1 - S_MIN)으로 센다.
3. 점수 = Σ k·w·y / (Σ k·w·|y| + PRIOR). y는 라벨의 좋고 싫음(-1~+1), w는 최근일수록 큰 가중치.
   분모에 |y|를 곱해, 약한 라벨(제목만 보고 지나침 -0.1 등)이 많아도 분명한 반응(±1)을 묻어 버리지 않게 한다.
   PRIOR가 있어 닮은 라벨이 적으면 점수가 0 쪽으로 줄어든다 (반응 하나로 순위가 크게 흔들리지 않게).
4. 닮은 라벨의 무게 합(support = Σ k·w·|y|)이 작으면 '아직 잘 모르는 영역'이다. 탐색 몫은 여기서 고른다.

한국어로 쓴 글과 영어 후보는 같은 사건이어도 유사도가 낮게 나온다(음역된 인물 이름 등: 0.5 안팎, 같은 언어면 0.8 이상).
그래서 라벨 글은 번역문과 원문을 함께 넣는다.

기준값은 2026-11-25 실측에서 정했다 (카드 129개 ↔ 수집 후보 1,604개, paraphrase-multilingual-MiniLM-L12-v2):
카드와 자기 원문 후보의 유사도 평균 0.69, 무관한 후보 중앙값 0.19, 카드끼리 상위 10% 경계 0.47.
→ S_MIN 0.45: 같은 사건·같은 주제쯤부터 닮았다고 본다.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path

MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"  # 약 220MB, 384차원, 한·영 혼합
CACHE = Path.home() / ".cache" / "ai-brief" / "fastembed"
S_MIN = 0.45
PRIOR = 1.0


@dataclass
class Label:
    key: str        # 라벨 글의 id
    texts: list[str]  # 임베딩할 글 내용. 같은 글의 여러 판(번역문과 원문 등)을 주면 그중 가장 닮은 것으로 비교한다
    y: float        # 좋고 싫은 정도: -1 ~ +1
    weight: float = 1.0  # 최근일수록 1에 가깝다
    note: str = ""  # 점수 근거에 붙일 짧은 설명 (예: "좋아요·주제가 좋음")


@dataclass
class Match:
    value: float    # -1 ~ +1
    support: float  # 닮은 라벨의 무게 합. 0이면 아직 모르는 영역
    neighbors: list[tuple[Label, float]] = field(default_factory=list)  # (라벨, 닮음 k), 영향 큰 순


class Embedder:
    """fastembed가 없거나 모델을 못 받으면 error에 이유를 남기고 None을 돌려준다 (순위표는 이 점수 없이 계속 만든다)."""

    def __init__(self, model: str = MODEL):
        self.model_name = model
        self._model = None
        self._memo: dict[str, object] = {}  # 같은 글을 여러 번 비교할 때(자동 조정의 되짚어 보기) 다시 계산하지 않는다
        self.error: str | None = None

    def embed(self, texts: list[str]):
        if self.error:
            return None
        try:
            import numpy as np
            from fastembed import TextEmbedding

            if self._model is None:
                self._model = TextEmbedding(self.model_name, cache_dir=str(CACHE))
            todo = list(dict.fromkeys(t for t in texts if t not in self._memo))
            for t, v in zip(todo, self._model.embed(todo)):
                v = np.asarray(v, dtype=np.float32)
                self._memo[t] = v / np.linalg.norm(v)
            return np.array([self._memo[t] for t in texts], dtype=np.float32)
        except Exception as exc:  # 설치 안 됨·모델 다운로드 실패·메모리 부족 등
            self.error = f"{type(exc).__name__}: {exc}"[:200]
            print(f"! 내용 유사도 꺼짐: {self.error}", file=sys.stderr)
            return None


class Taste:
    def __init__(self, labels: list[Label], embedder: Embedder | None = None):
        self.labels = [l for l in labels if abs(l.y) > 0.05 and any(x.strip() for x in l.texts)]
        self.embedder = embedder or Embedder()
        texts = [(i, x) for i, l in enumerate(self.labels) for x in l.texts if x.strip()]
        self._owner = [i for i, _ in texts]  # 임베딩 행 → 라벨 번호
        self._vecs = self.embedder.embed([x for _, x in texts]) if texts else None

    @property
    def ready(self) -> bool:
        return self._vecs is not None

    def match_many(self, texts: list[str]) -> list[Match]:
        empty = [Match(0.0, 0.0) for _ in texts]
        if not self.ready or not texts:
            return empty
        cand = self.embedder.embed(texts)
        if cand is None:
            return empty
        import numpy as np

        sims = cand @ self._vecs.T  # 후보 × 라벨 글의 판
        best = np.full((len(texts), len(self.labels)), -1.0, dtype=np.float32)
        for col, owner in enumerate(self._owner):
            best[:, owner] = np.maximum(best[:, owner], sims[:, col])
        k = np.clip((best - S_MIN) / (1 - S_MIN), 0, None)  # 후보 × 라벨
        y = np.array([l.y for l in self.labels])
        w = np.array([l.weight for l in self.labels]) * np.abs(y)
        sign = np.sign(y)
        out = []
        for row in k:
            kw = row * w
            support = float(kw.sum())
            value = float((kw * sign).sum() / (support + PRIOR))
            idx = [i for i in np.argsort(-kw) if kw[i] > 0][:3]
            out.append(Match(value, support, [(self.labels[i], float(row[i])) for i in idx]))
        return out
