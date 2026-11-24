"""원문 페이지에서 그림 후보를 뽑는다 (글쓰기 작업이 카드·긴 글에 붙일 그림을 고르는 용도).

사용: python3 collector/figures.py <원문 URL> [--download 폴더]
결과: 후보마다 번호, 그림 주소, 크기, 설명(figcaption·alt)을 출력한다.
      --download를 주면 후보를 폴더에 01.png, 02.jpg …로 내려받는다. 글쓰기 작업이 직접 열어 보고 고르기 위해서다.
      내려받은 파일은 확인용이다. 저장소에 커밋하지 않는다 — 사이트는 원본 주소를 그대로 가리킨다 (WRITING.md 3-1).

뽑는 곳: 대표 이미지(og:image·twitter:image), <figure> 안 그림과 설명, 본문 <img>.
로고·아이콘·프로필 사진처럼 정보가 없는 작은 그림과 svg는 뺀다.
외부 패키지 없이 표준 라이브러리만 쓴다 (collect.py와 같은 이유).
"""
from __future__ import annotations

import argparse
import html
import re
import struct
import sys
import time
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path

from collect import USER_AGENT, fetch

ICON_SIDE = 120  # 페이지에 적힌 긴 변이 이보다 작으면 아이콘으로 본다 (논문 HTML은 표시 크기를 작게 적는다)
DOWNLOAD_SECONDS = 20  # 그림 하나를 받는 전체 시간 상한 (조금씩 흘려보내는 서버가 있어 소켓 timeout만으로는 못 막는다)
DOWNLOAD_BYTES = 15_000_000
TARGET_WIDTH = 1400  # srcset에서 고를 너비: 본문 폭 680px의 약 2배 (고해상도 화면)
MAX_CANDIDATES = 12
SKIP_WORDS = re.compile(r"logo|icon|avatar|sprite|favicon|badge|emoji|pixel|spacer|placeholder|gravatar|profile", re.I)
ARXIV_ABS = re.compile(r"arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5}(?:v\d+)?)")


@dataclass
class Candidate:
    src: str
    caption: str = ""
    alt: str = ""
    origin: str = ""  # og:image / figure / img
    width: int | None = None
    height: int | None = None
    file: str = ""
    notes: list[str] = field(default_factory=list)


def _int(v: str | None) -> int | None:
    m = re.match(r"\s*(\d+)", v or "")
    return int(m.group(1)) if m else None


def _best_from_srcset(srcset: str) -> str | None:
    """srcset("a.png 640w, b.png 1280w")에서 TARGET_WIDTH 이상 중 가장 작은 것, 없으면 가장 큰 것을 고른다."""
    sizes = []
    for part in srcset.split(","):
        bits = part.strip().split()
        if bits:
            sizes.append(((_int(bits[1]) if len(bits) > 1 and bits[1].endswith("w") else 0) or 0, bits[0]))
    if not sizes:
        return None
    big_enough = [s for s in sizes if s[0] >= TARGET_WIDTH]
    return min(big_enough)[1] if big_enough else max(sizes)[1]


class FigureParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.meta: list[str] = []
        self.images: list[Candidate] = []
        self._figure: list[Candidate] | None = None  # 지금 열려 있는 <figure> 안 그림들
        self._caption: list[str] | None = None
        self._skip_depth = 0  # <nav>·<header>·<footer>·<aside> 안 그림은 본문이 아니다

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = {k: v or "" for k, v in attrs}
        if tag in ("nav", "header", "footer", "aside"):
            self._skip_depth += 1
        elif tag == "meta" and (a.get("property") or a.get("name")) in ("og:image", "og:image:url", "twitter:image"):
            if a.get("content"):
                self.meta.append(a["content"])
        elif tag == "figure":
            self._figure = []
        elif tag == "figcaption" and self._figure is not None:
            self._caption = []
        elif tag in ("img", "source") and not self._skip_depth:
            src = _best_from_srcset(a.get("srcset") or a.get("data-srcset") or "") or a.get("data-src") or a.get("src")
            if not src or tag == "source" and self._figure is None:
                return
            c = Candidate(src=src, alt=a.get("alt", ""), origin="figure" if self._figure is not None else "img",
                          width=_int(a.get("width")), height=_int(a.get("height")))
            if self._figure is not None:
                self._figure.append(c)
            self.images.append(c)

    def handle_endtag(self, tag: str) -> None:
        if tag in ("nav", "header", "footer", "aside") and self._skip_depth:
            self._skip_depth -= 1
        elif tag == "figcaption" and self._caption is not None and self._figure is not None:
            text = re.sub(r"\s+", " ", "".join(self._caption)).strip()
            for c in self._figure:
                c.caption = c.caption or text
            self._caption = None
        elif tag == "figure":
            self._figure = None

    def handle_data(self, data: str) -> None:
        if self._caption is not None:
            self._caption.append(data)


def page_url(url: str) -> str:
    """그림이 실제로 있는 페이지 주소. arXiv 초록 페이지는 그림이 없어 HTML 판으로 바꾼다."""
    m = ARXIV_ABS.search(url)
    return f"https://arxiv.org/html/{m.group(1)}" if m else url


def candidates(url: str) -> list[Candidate]:
    base = page_url(url)
    parser = FigureParser()
    parser.feed(fetch(base))
    found: list[Candidate] = [Candidate(src=s, origin="og:image") for s in parser.meta] + parser.images
    out, seen = [], set()
    for c in found:
        c.src = urllib.parse.urljoin(base, html.unescape(c.src.strip()))
        key = c.src.split("?")[0]
        if not c.src.startswith("http") or key in seen:
            continue
        seen.add(key)
        if key.lower().endswith(".svg") or SKIP_WORDS.search(key) or SKIP_WORDS.search(c.alt):
            continue
        if max(c.width or 0, c.height or 0) and max(c.width or 0, c.height or 0) < ICON_SIDE:
            continue
        out.append(c)
    # 설명이 달린 본문 그림이 가장 쓸모 있다 → 그다음 대표 이미지 → 나머지 본문 그림
    out.sort(key=lambda c: 0 if c.caption else 1 if c.origin == "og:image" else 2)
    return out[:MAX_CANDIDATES]


def image_size(data: bytes) -> tuple[int, int] | None:
    """PNG·GIF·JPEG·WebP 머리말에서 가로·세로를 읽는다."""
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return struct.unpack(">II", data[16:24])
    if data[:6] in (b"GIF87a", b"GIF89a"):
        return struct.unpack("<HH", data[6:10])
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        kind = data[12:16]
        if kind == b"VP8X":
            return 1 + int.from_bytes(data[24:27], "little"), 1 + int.from_bytes(data[27:30], "little")
        if kind == b"VP8 ":
            w, h = struct.unpack("<HH", data[26:30])
            return w & 0x3FFF, h & 0x3FFF
        if kind == b"VP8L":
            b = data[21:25]
            return 1 + (((b[1] & 0x3F) << 8) | b[0]), 1 + (((b[3] & 0xF) << 10) | (b[2] << 2) | ((b[1] & 0xC0) >> 6))
    if data[:2] == b"\xff\xd8":
        i = 2
        while i + 9 < len(data):
            if data[i] != 0xFF:
                i += 1
                continue
            marker = data[i + 1]
            if marker in (0xC0, 0xC1, 0xC2):
                h, w = struct.unpack(">HH", data[i + 5:i + 9])
                return w, h
            i += 2 + struct.unpack(">H", data[i + 2:i + 4])[0]
    return None


EXT = {b"\x89P": ".png", b"GI": ".gif", b"RI": ".webp", b"\xff\xd8": ".jpg"}


def download(c: Candidate, folder: Path, n: int, referer: str) -> None:
    req = urllib.request.Request(c.src, headers={"User-Agent": USER_AGENT, "Referer": referer})
    deadline = time.monotonic() + DOWNLOAD_SECONDS
    chunks: list[bytes] = []
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            while chunk := resp.read(65536):
                chunks.append(chunk)
                if time.monotonic() > deadline or sum(map(len, chunks)) > DOWNLOAD_BYTES:
                    raise TimeoutError(f"{DOWNLOAD_SECONDS}초·{DOWNLOAD_BYTES // 1_000_000}MB 상한 초과")
    except Exception as e:  # 그림 하나가 막혀도 나머지는 계속 받는다
        c.notes.append(f"내려받기 실패: {e}")
        return
    data = b"".join(chunks)
    size = image_size(data)
    if size:
        c.width, c.height = size
    path = folder / f"{n:02d}{EXT.get(data[:2], '.img')}"
    path.write_bytes(data)
    c.file = str(path)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("url")
    ap.add_argument("--download", metavar="폴더", help="후보를 이 폴더에 내려받는다 (확인용)")
    args = ap.parse_args()
    try:
        found = candidates(args.url)
    except Exception as e:
        print(f"페이지를 열 수 없음: {e}", file=sys.stderr)
        return 1
    if not found:
        print("그림 후보 없음")
        return 0
    folder = Path(args.download) if args.download else None
    if folder:
        folder.mkdir(parents=True, exist_ok=True)
    for n, c in enumerate(found, 1):
        if folder:
            download(c, folder, n, page_url(args.url))
        size = f"{c.width}×{c.height}" if c.width and c.height else "크기 모름"
        print(f"[{n:02d}] {c.origin} · {size}")
        print(f"     src: {c.src}")
        for label, text in (("설명", c.caption), ("alt", c.alt), ("파일", c.file), *(("주의", x) for x in c.notes)):
            if text:
                print(f"     {label}: {text[:300]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
