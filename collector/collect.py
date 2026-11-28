"""뉴스 후보 수집기.

sources.json의 출처를 돌면서 새 글을 data/inbox/<KST 날짜>.jsonl에 한 줄씩 쌓는다.
이미 본 글은 data/seen.json으로 거른다. 글쓰기(선별·작성)는 하지 않는다 — WRITING.md를 따르는 예약 작업의 몫.

외부 패키지 없이 표준 라이브러리만 쓴다 (GitHub Actions에서 설치 단계 없이 돌리기 위해).
사용: python3 collector/collect.py [--only 출처id,...] [--dry-run]
"""
from __future__ import annotations

import argparse
import datetime as dt
import email.utils
import gzip
import hashlib
import html
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCES = ROOT / "collector" / "sources.json"
DATA = ROOT / "data"
INBOX = DATA / "inbox"
SEEN = DATA / "seen.json"
DC_SIGNALS = DATA / "dc_signals.json"  # 특갤 X 링크 글의 최신 추천·조회 수 (rank.py가 화제성 점수에 씀)

KST = dt.timezone(dt.timedelta(hours=9))
USER_AGENT = "ai-brief-collector/0.1"  # URL을 덧붙이면 Techmeme이 휴대폰용 간이 페이지(기사별 X 토론 없음)를 준다
MAX_AGE = dt.timedelta(days=2)
VIDEO_MAX_AGE = dt.timedelta(days=4)   # 인터뷰·팟캐스트 영상은 퍼지는 데 며칠 걸려 더 넓게 본다        # 이보다 오래된 글은 후보로 넣지 않는다 (WRITING.md 2절 신선도 기준과 맞춤)
SEEN_TTL = dt.timedelta(days=21)      # seen 기록 보존 기간
SUMMARY_LIMIT = 600                   # 후보 요약 최대 글자 수 (원문 전체를 저장하지 않는다)
DC_POSTS_PER_RUN = 20                 # 디시 본문 요청 상한 (과요청 차단 방지)
DC_LIST_PAGES = 2                     # 특갤 "x.com" 검색 결과를 몇 쪽까지 볼지 (쪽당 20개)
TM_TWEETS_PER_STORY = 5               # Techmeme 기사 하나당 가져올 X 토론 글 수
TM_TWEETS_PER_RUN = 80                # Techmeme X oEmbed 요청 상한
DC_DELAY_SEC = 2.0
DRY_RUN = False  # --dry-run이면 어떤 파일도 쓰지 않는다
X_STATUS = re.compile(r"(?:x|twitter)\.com/([A-Za-z0-9_]{1,15})/status/(\d{15,20})")


# ---------- 공통 ----------

def now_utc() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def fetch(url: str, timeout: int = 25) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read()
        charset = resp.headers.get_content_charset() or "utf-8"
    if raw[:2] == b"\x1f\x8b":  # 요청하지 않아도 gzip으로 주는 서버가 있다 (DeepMind)
        raw = gzip.decompress(raw)
    return raw.decode(charset, "replace")


def item_id(url: str) -> str:
    return hashlib.sha1(url.encode("utf-8")).hexdigest()[:16]


def clean_text(s: str | None, limit: int = SUMMARY_LIMIT) -> str:
    if not s:
        return ""
    s = re.sub(r"<(script|style)[\s\S]*?</\1>", " ", s, flags=re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    s = re.sub(r"\s+", " ", s).strip()
    return s if len(s) <= limit else s[: limit - 1].rstrip() + "…"


def parse_date(s: str | None, naive_tz: dt.tzinfo = dt.timezone.utc) -> dt.datetime | None:
    """시간대 표기가 없는 날짜는 naive_tz로 본다 (국내 피드는 KST를 표기 없이 준다).

    시각 없이 날짜만 주는 피드(Nature·Cell 계열 학술지)는 0시로 읽으면 실제 공개보다 최대 하루 오래된 것으로 계산돼
    신선도 기준(WRITING.md 2절)에서 밀린다. 그래서 '지금'(= 처음 본 시각, 글은 seen.json으로 한 번만 받는다)과
    그날 끝 중 이른 쪽을 쓴다. 수집이 2시간마다 돌아 실제 공개 시각과 가깝고, 지난 날짜는 그대로 오래된 글이 된다.
    """
    if not s:
        return None
    s = s.strip()
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", s):
        day_end = dt.datetime.fromisoformat(s).replace(tzinfo=naive_tz) + dt.timedelta(days=1)
        return min(now_utc(), day_end.astimezone(dt.timezone.utc))
    try:
        d = email.utils.parsedate_to_datetime(s)
    except (TypeError, ValueError):
        try:
            d = dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
        except ValueError:
            return None
    if d.tzinfo is None:
        d = d.replace(tzinfo=naive_tz)
    return d.astimezone(dt.timezone.utc)


def snowflake_time(status_id: str) -> dt.datetime:
    ms = (int(status_id) >> 22) + 1288834974657
    return dt.datetime.fromtimestamp(ms / 1000, dt.timezone.utc)


# ---------- RSS / Atom ----------

def _local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _child_text(el: ET.Element, *names: str) -> str | None:
    for child in el:
        if _local(child.tag) in names and (child.text or "").strip():
            return child.text
    return None


def _atom_link(el: ET.Element) -> str | None:
    fallback = None
    for child in el:
        if _local(child.tag) != "link":
            continue
        href = child.get("href")
        if href and child.get("rel", "alternate") == "alternate":
            return href
        fallback = fallback or href or (child.text or "").strip() or None
    return fallback


def parse_feed(text: str, naive_tz: dt.tzinfo = dt.timezone.utc) -> list[dict]:
    text = re.sub(r"^[^<]+", "", text)  # BOM·공백 등 선행 잡음
    root = ET.fromstring(text)
    entries = [el for el in root.iter() if _local(el.tag) in ("item", "entry")]
    out = []
    for el in entries:
        title = clean_text(_child_text(el, "title"), 300)
        link = _atom_link(el) or _child_text(el, "link", "guid")
        date = parse_date(_child_text(el, "pubDate", "published", "updated", "date"), naive_tz)
        summary = clean_text(_child_text(el, "description", "summary", "content", "encoded"))
        if not summary:  # 유튜브 피드는 설명이 media:group 안에 있다
            desc = next((d.text for d in el.iter() if _local(d.tag) == "description" and d.text), None)
            summary = clean_text(desc)
        if title and link:
            out.append({"title": title, "url": link.strip(), "published": date, "summary": summary})
    return out


def collect_rss(src: dict) -> list[dict]:
    items = []
    naive_tz = KST if src.get("timezone") == "KST" else dt.timezone.utc
    max_age = VIDEO_MAX_AGE if src.get("video") else MAX_AGE
    for e in parse_feed(fetch(src["url"]), naive_tz):
        if e["published"] and now_utc() - e["published"] > max_age:
            continue
        if src.get("video") and "/shorts/" in e["url"]:
            continue  # 쇼츠는 발언 확인이 어려워 뺀다
        item = make_item(src, e["title"], e["url"], e["published"], e["summary"])
        if src.get("video"):
            item["video"] = True
        items.append(item)
    return items


# ---------- Hugging Face Daily Papers ----------

def collect_hf_papers(src: dict) -> list[dict]:
    items = []
    for p in json.loads(fetch(src["url"])):
        paper = p.get("paper", {})
        pid = paper.get("id")
        if not pid:
            continue
        url = f"https://huggingface.co/papers/{pid}"
        published = parse_date(p.get("publishedAt") or paper.get("publishedAt"))
        summary = clean_text(paper.get("summary"))
        item = make_item(src, clean_text(paper.get("title"), 300), url, published, summary)
        item["upvotes"] = paper.get("upvotes")
        items.append(item)
    return items


# ---------- 새 기술 출처 (허깅페이스 급상승 모델, GitHub 급상승 저장소, RSS 없는 공식 뉴스 페이지) ----------

AI_REPO = re.compile(r"\b(ai|llm|gpt|claude|gemini|agent|agentic|model|transformer|diffusion|rag|inference|robot|neural|mcp)\b|인공지능|大模型|模型", re.I)


def collect_hf_models(src: dict) -> list[dict]:
    """허깅페이스 급상승 모델 중 최근 MAX_AGE 안에 올라온 것 — 막 나온 오픈 모델."""
    items = []
    for m in json.loads(fetch(src["url"])):
        created = parse_date(m.get("createdAt"))
        if not created or now_utc() - created > MAX_AGE:
            continue
        mid = m["id"]
        if re.search(r"gguf|uncensored|abliterated|-awq|-gptq|exl2|mlx", mid, re.I):
            continue  # 원본이 아닌 변환·파생본은 뺀다
        summary = f"허깅페이스 급상승 점수 {m.get('trendingScore', 0):.0f}, 좋아요 {m.get('likes', 0)}, 분야 {m.get('pipeline_tag') or '-'}"
        item = make_item(src, mid, f"https://huggingface.co/{mid}", created, summary)
        item["trending"] = m.get("trendingScore")
        items.append(item)
    return items


def collect_gh_trending(src: dict) -> list[dict]:
    """GitHub 오늘의 급상승 저장소 중 AI 관련만."""
    page = fetch(src["url"])
    items = []
    for art in re.findall(r'<article class="Box-row">([\s\S]*?)</article>', page):
        name = re.search(r'<h2[^>]*>\s*<a[^>]*href="/([^"]+)"', art)
        desc = re.search(r'<p class="col-9[^"]*">([\s\S]*?)</p>', art)
        stars = re.search(r"([\d,]+) stars today", art)
        if not name:
            continue
        repo, d = name.group(1).strip(), clean_text(desc.group(1), 300) if desc else ""
        if not AI_REPO.search(repo + " " + d):
            continue
        today = int(stars.group(1).replace(",", "")) if stars else 0
        # 급상승 목록은 '오늘' 기준이라 수집 시각을 발표 시각으로 쓴다 (같은 저장소는 seen으로 한 번만)
        item = make_item(src, f"{repo} — {d}"[:200], f"https://github.com/{repo}", now_utc(), f"오늘 별 {today}개. {d}")
        item["stars_today"] = today
        items.append(item)
    return items


def collect_page_links(src: dict) -> list[dict]:
    """RSS가 없는 공식 뉴스 목록 페이지에서 글 링크·제목·날짜를 읽는다 (예: Anthropic)."""
    page = fetch(src["url"])
    base = re.match(r"https?://[^/]+", src["url"]).group(0)
    items = {}
    for m in re.finditer(r'<a[^>]*href="(' + re.escape(src["path_prefix"]) + r'[a-z0-9-]+)"[^>]*>([\s\S]*?)</a>', page):
        text = clean_text(m.group(2), 400)
        date = re.search(r"([A-Z][a-z]{2} \d{1,2}, \d{4})", text)
        if not date:
            continue  # 날짜 없는 링크는 분류 메뉴 등
        published = dt.datetime.strptime(date.group(1), "%b %d, %Y").replace(tzinfo=dt.timezone.utc)
        if now_utc() - published > MAX_AGE:
            continue
        title = re.sub(r"\s*" + re.escape(date.group(1)) + r"\s*", " ", text).strip()
        url = base + m.group(1)
        items[url] = make_item(src, title[:200], url, published, "")
    return list(items.values())


# ---------- 유튜브 인물 검색 (YouTube Data API, 무료 할당량) ----------

YT_STATE = DATA / "yt_state.json"


def _yt_due(src: dict, state: dict) -> bool:
    """출처마다 마지막 검색 후 interval_hours(기본 3.5시간)가 지났나. 수동 실행이 겹쳐도 할당량을 넘지 않게."""
    last = state.get(src["id"]) or (state.get("last_search") if src["id"] == "yt-people" else None)  # 예전 키
    hours = src.get("interval_hours", 3.5)
    if last and now_utc() - dt.datetime.fromisoformat(last) < dt.timedelta(hours=hours):
        print(f"  ({src['name']}: 마지막 검색 {last} — {hours}시간 안 지나 건너뜀)", file=sys.stderr)
        return False
    return True


def collect_youtube_search(src: dict) -> list[dict]:
    """유튜브 검색으로 채널 구독이 못 따라가는 영상을 찾는다. 출처 설정에 따라 두 가지:
    - people: 핵심 인물 이름으로 한 명씩 (강연·인터뷰는 매번 다른 채널에 올라온다. 여러 명을 묶으면 상위 몇 개에 묻힌다)
    - queries + order viewCount: 사람을 정하지 않고, 최근 AI 인터뷰·강연 중 조회수가 높은 것
      (재가공 클립 채널까지 — 누가 나오든 지금 퍼지고 있는 영상을 잡는다)
    할당량: 검색 1회 = 100 단위, 하루 무료 10,000. 인물 12명 × 하루 6회 = 7,200, 조회수 검색 3개 × 하루 3회 = 900.
    YOUTUBE_API_KEY 환경변수가 없으면 건너뛴다."""
    key = os.environ.get("YOUTUBE_API_KEY")
    if not key:
        print(f"  (YOUTUBE_API_KEY 없음 — {src['name']} 건너뜀)", file=sys.stderr)
        return []
    state = json.loads(YT_STATE.read_text()) if YT_STATE.exists() else {}
    if not _yt_due(src, state):
        return []
    after = (now_utc() - VIDEO_MAX_AGE).strftime("%Y-%m-%dT%H:%M:%SZ")
    order = src.get("order", "relevance")
    searches = [(f'"{p}"', p) for p in src.get("people", [])] + [(q, None) for q in src.get("queries", [])]
    found: dict[str, tuple[dict, str | None]] = {}
    for q, person in searches:
        params = urllib.parse.urlencode({"part": "snippet", "type": "video", "q": q, "publishedAfter": after,
                                         "order": order, "maxResults": src.get("max_results", 8),
                                         "relevanceLanguage": "en", "key": key})
        for it in json.loads(fetch(f"https://www.googleapis.com/youtube/v3/search?{params}")).get("items", []):
            found.setdefault(it["id"]["videoId"], (it["snippet"], person))
    if not DRY_RUN:
        state.pop("last_search", None)
        state[src["id"]] = now_utc().isoformat()
        YT_STATE.write_text(json.dumps(state))
    if not found:
        return []
    stats: dict[str, dict] = {}
    ids = list(found)
    for k in range(0, len(ids), 50):
        params = urllib.parse.urlencode({"part": "statistics,contentDetails", "id": ",".join(ids[k:k + 50]), "key": key})
        stats.update({v["id"]: v for v in json.loads(fetch(f"https://www.googleapis.com/youtube/v3/videos?{params}")).get("items", [])})
    items = []
    for vid, (sn, person) in found.items():
        st = stats.get(vid, {})
        if not re.search(r"\d+M|\d+H", st.get("contentDetails", {}).get("duration", "")):
            continue  # 1분 미만 쇼츠 제외
        if person and person.split()[-1].lower() not in (sn.get("title", "") + " " + sn.get("description", "")).lower():
            continue  # 이름이 실제로 나오지 않는 영상(드라마 등) 제외
        views = int(st.get("statistics", {}).get("viewCount", 0))
        if views < src.get("min_views", 0):
            continue
        url = f"https://www.youtube.com/watch?v={vid}"
        who = f" · 인물 {person}" if person else ""
        summary = f"{sn.get('channelTitle', '')} · 조회 {views:,}{who} · {clean_text(sn.get('description'), 400)}"
        item = make_item(src, clean_text(sn.get("title"), 200), url, parse_date(sn.get("publishedAt")), summary)
        item.update({"video": True, "views": views, "channel": sn.get("channelTitle")})
        if person:
            item["person"] = person
        items.append(item)
    return items


# ---------- 인기 팟캐스트 차트 ----------

PODCAST_STATE = DATA / "podcast_charts.json"


def podcast_chart_ranks(src: dict) -> dict[str, int]:
    """애플 팟캐스트 분야별 상위 차트: 쇼 id → 순위 (여러 분야에 들면 높은 쪽). 하루에 한 번만 새로 받는다."""
    state = json.loads(PODCAST_STATE.read_text()) if PODCAST_STATE.exists() else {}
    if state.get("ranks") and now_utc() - dt.datetime.fromisoformat(state["fetched"]) < dt.timedelta(days=1):
        return state["ranks"]
    ranks: dict[str, int] = {}
    for genre in src["genres"]:
        url = f"https://itunes.apple.com/{src.get('country', 'us')}/rss/toppodcasts/limit={src['top']}/genre={genre}/json"
        for pos, e in enumerate(json.loads(fetch(url))["feed"].get("entry", []), 1):
            sid = e["id"]["attributes"]["im:id"]
            ranks[sid] = min(pos, ranks.get(sid, pos))
    if ranks and not DRY_RUN:
        PODCAST_STATE.write_text(json.dumps({"fetched": now_utc().isoformat(), "ranks": ranks}))
    return ranks


def collect_podcast_chart(src: dict) -> list[dict]:
    """인기 팟캐스트 차트(애플 기술·비즈니스 분야 상위)에 든 쇼의 최신 에피소드.
    사람이나 쇼를 손으로 고르지 않는다 — 많이 듣는 쇼가 차트에 오르면 저절로 구독된다.
    피드 전체(수 MB) 대신 애플 조회 API로 쇼마다 최신 에피소드 몇 개만 받는다 (요청 50쇼당 1번).
    AI·기술과 무관한 에피소드는 순위표의 broad 관문이 가린다. 차트 전체를 받으면 하루 수십 편이라
    출처 등급은 대량 집계(0)로 두고, 순위표가 차트 순위(chart_rank)로 화제성 점수를 준다."""
    ranks = podcast_chart_ranks(src)
    ids = list(ranks)
    items = []
    for k in range(0, len(ids), 50):
        q = urllib.parse.urlencode({"id": ",".join(ids[k:k + 50]), "entity": "podcastEpisode", "limit": src.get("episodes", 3)})
        for r in json.loads(fetch(f"https://itunes.apple.com/lookup?{q}")).get("results", []):
            if r.get("wrapperType") != "podcastEpisode":
                continue
            published = parse_date(r.get("releaseDate"))
            if not published or now_utc() - published > VIDEO_MAX_AGE:
                continue
            title = f"{r.get('collectionName', '')} — {r.get('trackName', '')}"
            item = make_item(src, clean_text(title, 200), r["trackViewUrl"].split("?")[0], published,
                             clean_text(r.get("description") or r.get("shortDescription")))
            item.update({"podcast": True, "channel": r.get("collectionName"),
                         "chart_rank": ranks.get(str(r.get("collectionId")))})
            items.append(item)
    return items


# ---------- 특갤 X 링크 레이더 ----------

def dc_x_post_list(gallery: str) -> list[dict]:
    posts = []
    for page_no in range(1, DC_LIST_PAGES + 1):
        q = urllib.parse.urlencode({"id": gallery, "s_type": "search_subject_memo", "s_keyword": "x.com", "page": page_no})
        if page_no > 1:
            time.sleep(DC_DELAY_SEC)
        posts.extend(_dc_rows(fetch(f"https://gall.dcinside.com/mgallery/board/lists/?{q}")))
    return list({p["no"]: p for p in posts}.values())


def _dc_rows(page: str) -> list[dict]:
    posts = []
    for row in re.finditer(r'<tr class="ub-content us-post[^"]*"[^>]*data-no="(\d+)"[\s\S]*?</tr>', page):
        block = row.group(0)
        if re.search(r'class="gall_subject"[^>]*>\s*(공지|설문)', block):
            continue
        title = re.search(r'class="gall_tit[^"]*"[\s\S]*?<a[^>]*>([\s\S]*?)</a>', block)
        date = re.search(r'class="gall_date"[^>]*title="([^"]+)"', block)
        rec = re.search(r'class="gall_recommend"[^>]*>\s*(\d+)', block)
        views = re.search(r'class="gall_count"[^>]*>\s*(\d+)', block)
        posts.append({
            "no": row.group(1),
            "title": clean_text(title.group(1), 200) if title else "",
            "date": date.group(1) if date else None,
            "recommend": int(rec.group(1)) if rec else 0,
            "views": int(views.group(1)) if views else 0,
        })
    return posts


def oembed(url: str) -> dict | None:
    q = urllib.parse.urlencode({"url": url, "omit_script": 1, "dnt": "true"})
    try:
        data = json.loads(fetch(f"https://publish.twitter.com/oembed?{q}"))
    except Exception:
        return None
    body = re.search(r"<p[^>]*>([\s\S]*?)</p>", data.get("html", ""))
    return {"author": data.get("author_name"), "text": clean_text(body.group(1), 1000) if body else ""}


def collect_dc_x(src: dict, seen: dict) -> list[dict]:
    gallery = src["gallery"]
    items = []
    fetched = 0
    posts = dc_x_post_list(gallery)
    update_dc_signals(gallery, posts)
    for post in posts:
        key = f"dc:{gallery}:{post['no']}"
        if key in seen:
            continue
        if fetched >= DC_POSTS_PER_RUN:
            break
        time.sleep(DC_DELAY_SEC)
        fetched += 1
        try:
            body = fetch(f"https://gall.dcinside.com/mgallery/board/view/?id={gallery}&no={post['no']}")
        except Exception as exc:
            print(f"  ! 디시 글 {post['no']} 실패: {exc}", file=sys.stderr)
            continue
        seen[key] = now_utc().isoformat()
        # 본문 영역(write_div ~ 추천 버튼)만 본다. 댓글·광고 속 링크는 제외.
        start = body.find('class="write_div"')
        end = body.find("btn_recommend_box", start)
        segment = body[start:end] if start >= 0 and end > start else ""
        for handle, sid in dict.fromkeys(X_STATUS.findall(segment)):
            url = f"https://x.com/{handle}/status/{sid}"
            posted = snowflake_time(sid)
            if now_utc() - posted > MAX_AGE:
                continue
            tweet = oembed(url) or {"author": None, "text": ""}
            item = make_item(src, tweet["text"][:120] or f"@{handle} 게시물", url, posted, tweet["text"])
            item["tweet"] = {"handle": handle, "author": tweet["author"], "text": tweet["text"], "url": url}
            # 특갤 글은 "무엇이 화제인가" 신호로만 남긴다. 본문은 저장하지 않는다.
            item["signal"] = {"title": post["title"], "url": f"https://gall.dcinside.com/mgallery/board/view/?id={gallery}&no={post['no']}"}
            items.append(item)
    return items


def update_dc_signals(gallery: str, posts: list[dict]) -> None:
    """목록에 보이는 글의 추천·조회 수를 매 실행 갱신한다. 글이 올라온 뒤 반응이 쌓이므로 처음 본 값으로 고정하지 않는다."""
    if DRY_RUN:
        return
    signals = json.loads(DC_SIGNALS.read_text()) if DC_SIGNALS.exists() else {}
    cutoff = now_utc() - SEEN_TTL
    signals = {k: v for k, v in signals.items() if dt.datetime.fromisoformat(v["updated"]) >= cutoff}
    for p in posts:
        url = f"https://gall.dcinside.com/mgallery/board/view/?id={gallery}&no={p['no']}"
        signals[url] = {"title": p["title"], "recommend": p["recommend"], "views": p["views"], "updated": now_utc().isoformat()}
    DC_SIGNALS.parent.mkdir(parents=True, exist_ok=True)
    DC_SIGNALS.write_text(json.dumps(signals, ensure_ascii=False, indent=0, sort_keys=True))


# ---------- Techmeme 기사별 X 토론 ----------

def collect_techmeme_x(src: dict, seen: dict) -> list[dict]:
    """Techmeme 첫 화면의 기사마다 붙은 X 글(헤드라인 자체가 트윗인 경우 포함)을 가져온다.
    기사 제목을 context로 남겨, 순위표가 같은 기사의 다른 출처와 묶을 수 있게 한다."""
    page = fetch(src["url"])
    blocks = [(m.start(), m.group(1)) for m in re.finditer(r'CLASS="itc2" ID="(\d{6}p\d+)"', page)]
    items = []
    budget = TM_TWEETS_PER_RUN
    for i, (start, sid) in enumerate(blocks):
        block = page[start: blocks[i + 1][0] if i + 1 < len(blocks) else len(page)]
        head = re.search(r'<STRONG CLASS="L\d+"><A[^>]*HREF="([^"]+)"[^>]*>([\s\S]*?)</A>', block)
        if not head:
            continue
        headline, head_url = clean_text(head.group(2), 300), head.group(1)
        story_url = f"https://www.techmeme.com/{sid[:6]}/p{sid.split('p')[1]}#a{sid}"
        tweets = []
        if m := X_STATUS.search(head_url):
            tweets.append((m.group(1), m.group(2), True))  # 기사 자체가 트윗 (발표 트윗)
        x_sec = re.search(r'<SPAN CLASS="drhed">X:</SPAN>([\s\S]*?)</span>', block)
        if x_sec:
            tweets += [(h, t, False) for h, t in X_STATUS.findall(x_sec.group(1))][:TM_TWEETS_PER_STORY]
        for handle, tid, is_headline in tweets:
            url = f"https://x.com/{handle}/status/{tid}"
            iid = item_id(url)
            if iid in seen or handle.lower() == "techmeme" or budget <= 0:
                continue
            posted = snowflake_time(tid)
            if now_utc() - posted > MAX_AGE:
                continue
            budget -= 1
            tweet = oembed(url) or {"author": None, "text": ""}
            item = make_item(src, tweet["text"][:120] or f"@{handle} 게시물", url, posted, tweet["text"])
            item["tweet"] = {"handle": handle, "author": tweet["author"], "text": tweet["text"], "url": url}
            item["context"] = {"title": headline, "url": story_url, "headline_tweet": is_headline}
            items.append(item)
    return items


# ---------- 조립 ----------

def make_item(src: dict, title: str, url: str, published: dt.datetime | None, summary: str) -> dict:
    return {
        "id": item_id(url),
        "source": src["id"],
        "source_name": src["name"],
        "category_hint": src["category"],
        "title": title,
        "url": url,
        "published": published.isoformat() if published else None,
        "collected": now_utc().isoformat(),
        "summary": summary,
    }


COLLECTORS = {"rss": collect_rss, "hf_papers": collect_hf_papers, "hf_models": collect_hf_models,
              "gh_trending": collect_gh_trending, "page_links": collect_page_links,
              "youtube_search": collect_youtube_search, "podcast_chart": collect_podcast_chart}


def load_seen() -> dict:
    if not SEEN.exists():
        return {}
    seen = json.loads(SEEN.read_text())
    cutoff = now_utc() - SEEN_TTL
    return {k: v for k, v in seen.items() if dt.datetime.fromisoformat(v) >= cutoff}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="쉼표로 구분한 출처 id만 실행")
    ap.add_argument("--dry-run", action="store_true", help="파일에 쓰지 않고 결과만 출력")
    args = ap.parse_args()
    global DRY_RUN
    DRY_RUN = args.dry_run

    sources = json.loads(SOURCES.read_text())["sources"]
    if args.only:
        wanted = set(args.only.split(","))
        sources = [s for s in sources if s["id"] in wanted]

    seen = load_seen()
    new_items: list[dict] = []
    failures = []
    for src in sources:
        try:
            if src["type"] == "dc_x_search":
                items = collect_dc_x(src, seen)
            elif src["type"] == "techmeme_x":
                items = collect_techmeme_x(src, seen)
            else:
                items = COLLECTORS[src["type"]](src)
        except Exception as exc:
            failures.append(src["id"])
            print(f"! {src['id']} 실패: {exc}", file=sys.stderr)
            continue
        fresh = []
        for it in items:  # 같은 실행 안의 중복(한 글이 같은 트윗을 여러 번 링크)도 거른다
            if it["id"] in seen:
                continue
            seen[it["id"]] = it["collected"]
            fresh.append(it)
        new_items.extend(fresh)
        print(f"{src['id']:20s} 새 글 {len(fresh)}")

    print(f"합계 새 글 {len(new_items)}, 실패 {len(failures)} {failures}")
    if args.dry_run:
        for it in new_items[:20]:
            print(json.dumps(it, ensure_ascii=False)[:300])
        return 0

    INBOX.mkdir(parents=True, exist_ok=True)
    day = now_utc().astimezone(KST).strftime("%Y-%m-%d")
    with (INBOX / f"{day}.jsonl").open("a", encoding="utf-8") as f:
        for it in new_items:
            f.write(json.dumps(it, ensure_ascii=False) + "\n")
    SEEN.write_text(json.dumps(seen, ensure_ascii=False, indent=0, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
