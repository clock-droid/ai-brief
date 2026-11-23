# AI 브리핑 (가제)

AI와 미래 산업 소식을 빠르게 모으고, 읽기 편한 카드와 긴 글로 정리해 싣는 사이트.

| 단계 | 담당 | 파일 |
|---|---|---|
| 수집 | GitHub Actions, 30분마다 | `collector/collect.py`, `collector/sources.json` → `data/inbox/` |
| 글쓰기 | Claude 클라우드 예약 작업 | `WRITING.md` 규칙 → `web/src/content/` |
| 배포 | GitHub Actions → GitHub Pages | `web/` (Astro) |

- 디자인 값: `web/DESIGN.md`
- 로컬 실행: `npm --prefix web run dev` 후 http://localhost:4321/ai-brief/
- 수집기 수동 실행: `python3 collector/collect.py --dry-run`
