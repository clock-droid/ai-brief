"""관심 점수의 자동 조정: 과거 반응으로 되짚어 보고(시간 분할 백테스트), 더 잘 맞히는 설정이 분명할 때만 바꾼다.

이 파일은 이 프로젝트의 파일·신호 형식을 모른다. 평가할 구간(Window)과 "설정 → 구간별 점수" 함수만 받는다.
구간을 만드는 일(어떤 글이 언제 보였고 어떻게 반응했나)은 preferences.py가 한다.

왜 필요한가: 손으로 정한 배율이 실제 반응을 잘 맞힌다는 보장이 없고, 반응이 쌓이면 맞는 설정도 바뀐다.
그래서 고정값 대신 매 실행 과거 반응으로 다시 고른다. (실측 수치는 공개 저장소에 적지 않는다.)

방법:
1. 구간마다 "그 시각 이전 신호만으로 만든 모델"이 "그 시각 이후 처음 보인 글"에 매긴 점수를 받는다.
2. 실제 반응 등급(좋아요 2, 열어 봄·원문 클릭 1, 지나침 0, 싫어요 -1)과 점수 순서가 맞는 쌍의 비율(일치도)을 잰다.
   0.5는 동전 던지기, 1은 완벽.
3. 후보 설정 중 평균 일치도가 가장 높은 것이 기본 설정보다 MARGIN 이상 높고 구간 과반에서 이겼을 때만 그 설정을 쓴다.
   평가할 구간이 모자라거나 차이가 작으면 기본 설정 그대로 둔다 (적은 표본에 흔들리지 않게).
"""
from __future__ import annotations

import itertools
from dataclasses import dataclass
from typing import Callable

MARGIN = 0.03


@dataclass(frozen=True)
class Config:
    content_pts: int    # 내용 유사도(-1~+1)를 점수로 옮기는 배율
    strong_only: bool   # 내용 유사도 라벨을 좋아요·싫어요를 누른 글로만 (읽은 기록·지나침 라벨 제외)
    site_pts: int       # 출처(도메인·X 계정)별 반응률 점수 배율
    cat_pts: int        # 분류별 반응률 점수 배율

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
    grades: list[float]  # 그 구간에 처음 보인 글들의 실제 반응 등급


def concordance(scores: list[float], grades: list[float]) -> float | None:
    """등급이 다른 글 쌍 중 점수 순서가 맞는 비율 (동점은 반). 쌍이 없으면 None."""
    good = total = 0.0
    for i, j in itertools.combinations(range(len(grades)), 2):
        if grades[i] == grades[j]:
            continue
        total += 1
        d = (scores[i] - scores[j]) * (grades[i] - grades[j])
        good += 1 if d > 0 else 0.5 if d == 0 else 0
    return good / total if total else None


@dataclass
class Choice:
    config: Config
    note: str  # 순위표 머리에 붙이는 한 줄 (공개 저장소에는 남지 않는 파일)


def choose(windows: list[Window], score: Callable[[Config, int], list[float]], min_windows: int = 2) -> Choice:
    """score(설정, 구간 번호) → 그 구간 글들의 점수 (windows[i].grades와 같은 순서)."""
    if len(windows) < min_windows:
        return Choice(DEFAULT, f"자동 조정 보류 (평가 구간 {len(windows)}개, {min_windows}개부터)")
    table: dict[Config, list[float | None]] = {
        cfg: [concordance(score(cfg, i), w.grades) for i, w in enumerate(windows)] for cfg in GRID
    }
    valid = [i for i in range(len(windows)) if table[DEFAULT][i] is not None]
    if len(valid) < min_windows:
        return Choice(DEFAULT, f"자동 조정 보류 (반응이 갈린 구간 {len(valid)}개)")

    def mean(cfg: Config) -> float:
        return sum(table[cfg][i] for i in valid) / len(valid)

    base = mean(DEFAULT)
    best = max(GRID, key=lambda c: (round(mean(c), 3), -c.size()))
    wins = sum(table[best][i] > table[DEFAULT][i] for i in valid)
    head = f"자동 조정: 기본 {DEFAULT.label()} 일치도 {base:.2f}"
    if best != DEFAULT and mean(best) >= base + MARGIN and wins * 2 > len(valid):
        return Choice(best, f"{head} → {best.label()} {mean(best):.2f} 채택 (구간 {len(valid)}개 중 {wins}개 우세)")
    return Choice(DEFAULT, f"{head}, 최고 {best.label()} {mean(best):.2f} — 차이가 작아 기본 유지")
