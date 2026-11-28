"""인터뷰·강연 출연자의 유명도: 제목에 나온 인물의 영어 위키백과 문서 최근 30일 조회수.

명단을 손으로 정하지 않는다. 제목에서 사람 이름처럼 보이는 낱말 묶음을 뽑고, 위키백과 요청 한 번(이름 50개씩)으로
① 문서가 있고 ② 생존 인물 분류(Category:Living people)에 들며 ③ 최근 30일 조회수가 몇인지 잰다.
누가 나와도 같은 잣대로 재므로, 처음 보는 출연자도 유명하면 점수를 받는다.
(위키데이터 질의 서비스는 장애 때 분당 1회로 막힌 적이 있어 쓰지 않는다. 인터뷰 출연자는 생존 인물이다.)

요청을 아끼려고 data/fame.json에 이름별 결과를 저장한다: 사람은 PERSON_TTL, 사람 아님·문서 없음은 OTHER_TTL 동안 다시 묻지 않는다.
위키미디어 API는 무료이고 키가 없다. 실패하면 점수 없이 넘어간다 (수집을 멈추지 않는다).
"""
from __future__ import annotations

import datetime as dt
import json
import re
import sys
import time
import urllib.parse
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "data" / "fame.json"
PERSON_TTL = dt.timedelta(days=7)
OTHER_TTL = dt.timedelta(days=30)
BATCH = 50          # 위키백과 API가 한 번에 받는 문서 수
DELAY_SEC = 7.0     # 요청 사이 간격. 연락처 없는 User-Agent는 분당 10회까지 (위키미디어 API 요청 한도, 2026)
MAX_REQUESTS = 12   # 한 번 실행에서 보내는 요청 수 상한 (약 1분 반). 못 다 물은 이름은 다음 실행에

# 이름 낱말: 대문자로 시작 (Reid, Fei-Fei, McKinsey, O'Brien), 또는 가운데 이니셜 (J.)
WORD = re.compile(r"[A-Z][a-z]*(?:[-'’][A-Z]?[a-z]+)*[a-z]|[A-Z]\.|[A-Z][a-z]*[A-Z][a-z]+")


def names_in(title: str) -> list[str]:
    """대문자 낱말이 이어진 구간마다 겹치는 2~3낱말 묶음을 모두 후보로 ("Conversation With Daniel Susskind" → … "Daniel Susskind").
    제목 낱말 대부분이 대문자인 영어 제목이라 후보가 많지만, 사람인지는 위키백과가 가린다."""
    out: list[str] = []
    for run in re.split(r"[^A-Za-z.'’\- ]+|\s[-–—]\s", title):
        words = run.split()
        start = 0
        for i in range(len(words) + 1):
            if i < len(words) and WORD.fullmatch(words[i]):
                continue
            seg = words[start:i]
            for n in (2, 3):
                out += [" ".join(seg[k:k + n]) for k in range(len(seg) - n + 1)]
            start = i + 1
    return list(dict.fromkeys(out))


def load_cache() -> dict[str, dict]:
    return json.loads(CACHE.read_text()) if CACHE.exists() else {}


def guests(cache: dict[str, dict], title: str) -> list[dict]:
    """제목에 나온 인물 중 위키백과에 있는 생존 인물: [{name, views}], 조회수 큰 순. 저장된 결과만 쓴다 (요청 없음)."""
    found = {cache[n]["title"]: cache[n]["views"] for n in names_in(title) if cache.get(n, {}).get("person")}
    return sorted(({"name": k, "views": v} for k, v in found.items()), key=lambda g: -g["views"])


class Fame:
    def __init__(self, fetch: Callable[[str], str], now: dt.datetime, dry_run: bool = False):
        self.fetch = fetch
        self.now = now
        self.dry_run = dry_run
        self.cache = load_cache()
        self.asked = 0
        self.requests = 0

    def _get(self, url: str) -> dict:
        if self.requests >= MAX_REQUESTS:
            raise RuntimeError("이번 실행 요청 상한")
        if self.requests:
            time.sleep(DELAY_SEC)
        self.requests += 1
        return json.loads(self.fetch(url))

    def _fresh(self, entry: dict | None) -> bool:
        if not entry:
            return False
        ttl = PERSON_TTL if entry.get("person") else OTHER_TTL
        return self.now - dt.datetime.fromisoformat(entry["checked"]) < ttl

    def _resolve(self, names: list[str]) -> None:
        """이름들을 위키백과 한 번에: 문서(넘겨주기 따라감) → 생존 인물 분류 → 최근 30일 조회수."""
        stamp = self.now.isoformat()
        params = {"action": "query", "format": "json", "redirects": 1, "prop": "categories|pageviews",
                  "clcategories": "Category:Living people", "cllimit": "max", "pvipdays": 30, "titles": "|".join(names)}
        data: dict = {"pages": {}}
        cont: dict = {}
        while True:  # 여러 문서를 한 번에 물으면 조회수는 나눠서 온다 (continue)
            res = self._get("https://en.wikipedia.org/w/api.php?" + urllib.parse.urlencode({**params, **cont}))
            part = res.get("query", {})
            for step in ("normalized", "redirects"):
                data.setdefault(step, part.get(step, []))
            for pid, page in part.get("pages", {}).items():
                merged = data["pages"].setdefault(pid, {"title": page["title"]})
                merged["categories"] = merged.get("categories") or page.get("categories")
                merged.setdefault("pageviews", {}).update(page.get("pageviews") or {})
            if "continue" not in res:
                break
            cont = res["continue"]
        alias = {n: n for n in names}
        for step in ("normalized", "redirects"):
            for m in data.get(step, []):
                for n, t in alias.items():
                    if t == m["from"]:
                        alias[n] = m["to"]
        pages = {p["title"]: p for p in data.get("pages", {}).values()}
        for n in names:
            page = pages.get(alias[n], {})
            if not page.get("categories"):
                self.cache[n] = {"person": False, "checked": stamp}
                continue
            views = sum(v or 0 for v in page.get("pageviews", {}).values())
            self.cache[n] = {"person": True, "title": page["title"], "views": views, "checked": stamp}

    def prepare(self, titles: list[str]) -> None:
        """여러 제목의 새 이름을 한꺼번에 확인한다 (이름 50개씩 묶어 요청). 실패하면 그 묶음은 다음 실행에서 다시."""
        todo = list(dict.fromkeys(n for t in titles for n in names_in(t) if not self._fresh(self.cache.get(n))))
        for k in range(0, len(todo), BATCH):
            try:
                self._resolve(todo[k:k + BATCH])
            except Exception as exc:  # 요청 상한·429 등: 남은 이름은 다음 실행에
                print(f"  (유명도 확인 {self.asked}/{len(todo)}개에서 멈춤: {exc})", file=sys.stderr)
                break
            self.asked += len(todo[k:k + BATCH])

    def save(self) -> None:
        if not self.dry_run:
            CACHE.write_text(json.dumps(self.cache, ensure_ascii=False, indent=0, sort_keys=True))
