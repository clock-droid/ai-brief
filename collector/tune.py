"""관심 점수의 자동 조정: 과거 반응으로 되짚어 보고(시간 분할 백테스트), 더 잘 맞히는 설정이 분명할 때만 바꾼다.

이 파일은 이 프로젝트의 파일·신호 형식을 모른다. 평가할 구간(Window: 실제 반응 등급과 설정별 재료)만 받는다.
구간을 만드는 일(어떤 글이 언제 보였고 어떻게 반응했나)은 preferences.py가 한다.

왜 필요한가: 손으로 정한 배율이 실제 반응을 잘 맞힌다는 보장이 없고, 반응이 쌓이면 맞는 설정도 바뀐다.
그래서 고정값 대신 매 실행 과거 반응으로 다시 고른다. (실측 수치는 공개 저장소에 적지 않는다.)

방법:
1. 하루 단위 구간마다 "그 날 전 신호만으로 만든 모델"이 "그 날 처음 보인 글"에 매긴 점수를 받는다.
   점수는 순위표와 똑같이 Config.points로 정수로 만든다 (되짚어 본 점수와 실제 순위표 점수가 어긋나지 않게).
2. 실제 반응 등급(좋아요 2, 열어 봄·원문 클릭 1, 지나침 0, 싫어요 -1)과 점수 순서가 맞는 쌍의 비율(일치도)을
   구간마다 재서 평균한다. 0.5는 동전 던지기, 1은 완벽.
3. 평균 일치도가 가장 높은 설정이 기본보다 MARGIN 이상 높아도, 우연인지 따로 확인한다.
   여러 설정 중 최고를 고르면 반응과 무관한 점수도 우연히 좋아 보이기 쉽다. 그래서 구간 안에서 반응 등급을
   PERM_N번 뒤섞어 "아무 관계 없을 때 최고 설정이 기본을 얼마나 앞서나"를 재고, 실제 차이가 그 분포의
   상위 PERM_P 안에 들 때만 채택한다 (최고를 고르는 과정까지 포함한 순열 검정).
"""
from __future__ import annotations

import itertools
from dataclasses import dataclass, field

MARGIN = 0.03
PERM_N = 200
PERM_P = 0.05
MIN_WINDOWS = 2


@dataclass(frozen=True)
class Config:
    content_pts: int    # 내용 유사도(-1~+1)를 점수로 옮기는 배율
    strong_only: bool   # 내용 유사도 라벨을 좋아요·싫어요를 누른 글로만 (읽은 기록·지나침 라벨 제외)
    site_pts: int       # 출처(도메인·X 계정)별 반응률(-1~+1) 배율
    cat_pts: int        # 분류별 반응률(-1~+1) 배율

    def points(self, content: float, site: float, cat: float) -> tuple[int, int, int]:
        """순위표에 더하는 (내용, 출처, 분류) 점수. 순위표와 자동 조정이 함께 쓴다."""
        return round(content * self.content_pts), round(site * self.site_pts), round(cat * self.cat_pts)

    def size(self) -> int:
        """단순한 정도: 켜진 항목 수. 일치도가 같으면 단순한 쪽을 고른다."""
        return (self.content_pts > 0) + self.strong_only + (self.site_pts > 0) + (self.cat_pts > 0)

    def label(self) -> str:
        return (f"내용×{self.content_pts}" + ("(반응 글만)" if self.strong_only else "")
                + f" 출처×{self.site_pts} 분류×{self.cat_pts}")


DEFAULT = Config(content_pts=4, strong_only=False, site_pts=0, cat_pts=0)  # 자동 조정 전부터 쓰던 설정
GRID = [Config(c, s, p, k) for c, s, p, k in itertools.product((0, 2, 4), (False, True), (0, 1, 2), (0, 1))
        if not (c == 0 and s)]  # 내용 점수를 끄면 라벨 종류는 뜻이 없다


@dataclass
class Window:
    name: str
    grades: list[float]                 # 그 구간에 처음 보인 글들의 실제 반응 등급
    content: dict[bool, list[float]]    # strong_only → 글별 내용 유사도
    site: list[float]                   # 글별 출처 반응률
    cat: list[float]                    # 글별 분류 반응률
    _cache: dict = field(default_factory=dict, repr=False)

    def scores(self, cfg: Config):
        if cfg not in self._cache:
            import numpy as np

            self._cache[cfg] = np.array([sum(cfg.points(c, s, k)) for c, s, k
                                         in zip(self.content[cfg.strong_only], self.site, self.cat)], dtype=float)
        return self._cache[cfg]


def concordance(scores, grades) -> float | None:
    """등급이 다른 글 쌍 중 점수 순서가 맞는 비율 (동점은 반). 쌍이 없으면 None."""
    import numpy as np

    s, g = np.asarray(scores, dtype=float), np.asarray(grades, dtype=float)
    dg = np.sign(g[:, None] - g[None, :])
    total = np.count_nonzero(dg)
    if not total:
        return None
    agree = np.sign(s[:, None] - s[None, :]) * dg
    return float(((agree > 0).sum() + 0.5 * ((agree == 0) & (dg != 0)).sum()) / total)


@dataclass
class Choice:
    config: Config
    note: str  # 순위표 머리에 붙이는 한 줄 (공개 저장소에 올라가지 않는 파일)


def choose(windows: list[Window], seed: int = 0) -> Choice:
    import numpy as np

    windows = [w for w in windows if concordance(w.scores(DEFAULT), w.grades) is not None]
    if len(windows) < MIN_WINDOWS:
        return Choice(DEFAULT, f"자동 조정 보류 (평가할 날 {len(windows)}일, {MIN_WINDOWS}일부터)")

    def means(grades: list) -> dict[Config, float]:
        out = {}
        for cfg in GRID:
            vals = [concordance(w.scores(cfg), g) for w, g in zip(windows, grades)]
            vals = [v for v in vals if v is not None]
            out[cfg] = sum(vals) / len(vals) if vals else 0.5
        return out

    real = means([np.asarray(w.grades) for w in windows])
    base = real[DEFAULT]
    best = max(GRID, key=lambda c: (round(real[c], 3), -c.size()))
    gap = real[best] - base
    head = f"자동 조정({len(windows)}일): 기본 {DEFAULT.label()} 일치도 {base:.2f}"
    if best == DEFAULT or gap < MARGIN:
        return Choice(DEFAULT, f"{head}, 최고 {best.label()} {real[best]:.2f} — 차이가 작아 기본 유지")
    rng = np.random.default_rng(seed)
    beaten = 0
    for _ in range(PERM_N):
        null = means([rng.permutation(w.grades) for w in windows])
        beaten += max(null.values()) - null[DEFAULT] >= gap
    p = (beaten + 1) / (PERM_N + 1)
    if p <= PERM_P:
        return Choice(best, f"{head} → {best.label()} {real[best]:.2f} 채택 (우연일 확률 {p:.0%})")
    return Choice(DEFAULT, f"{head}, 최고 {best.label()} {real[best]:.2f} — 우연일 확률 {p:.0%}라 기본 유지")
