# GPT가 추가한 당사자 원문 수집

Mac의 기존 자막 예약 작업이 같은 비공개 전달 폴더에 `gpt-primary-sources.json`을 쓴다. 클라우드에서 실행하는 기존 순위표가 이 파일과 등록된 개인 RSS의 후보를 읽는다. 편집자는 원문을 확인하고 카드 게재를 결정한다.

- `sources.json`에서 X 작성자와 최신 대화 검색식을 편집한다. 작성자는 X 검색 대신 계정의 게시물 탭(리트윗 제외, 인용 포함)으로 읽는다. 게시물 탭에는 답글이 없다. 대화 검색식은 3시간마다만 실행하고, 한 번 실패하면 하루 동안 멈춘다(검색이 막힌 계정을 반복 호출하지 않기 위해). 블로그 RSS는 기존 `collector/sources.json`에 등록한 뒤 그 출처 ID를 `existing_blog_sources`에 추가한다. RSS가 없는 슈미트 블로그는 공개 목록의 날짜를 그대로 보존한다.
- Mac에 X 로그인 상태의 Aside와 CLI가 필요하다. 최근 24시간으로 처음 조회하고, 이후에는 검색별 마지막 완료 시각부터 10분 겹쳐 확인한다. 검색별 최대 5페이지에 도달하면 부분 조회라고 기록한다. 429 응답이 오면 X 요청을 멈추고 다음 회차에 오래된 검색부터 이어간다. 답글은 최대 두 단계의 앞선 글을 확인한다. 읽을 수 없는 상위 글은 편집자가 원문 링크에서 확인한다. 비공개 전달 파일에는 로그인 없이 X 공개 임베드로 확인한 글의 발췌만 보낸다.
- 출력의 시간과 경고를 보면 Mac 중단·검색 실패와 새 글이 없는 경우를 구별할 수 있다. 순위표에서 같은 X 상태 ID는 계정명의 대소문자가 달라도 중복으로 처리한다.

운영과 분리된 미리보기:

```sh
preview_dir=$(mktemp -d)
python3 collector/gpt_primary_sources/capture.py "$preview_dir"
python3 collector/rank.py --primary-dir "$preview_dir"
```

GPT 기능은 `[GPT] Add direct researcher source collection` 한 커밋이다. 그 커밋을 `git revert`하면 Mac 수집 연결, 편집 지침, 순위표 변경도 함께 돌아간다. 비공개 전달 파일까지 지우려면 기능을 되돌린 뒤 해당 저장소에서 `gpt-primary-sources.json`만 삭제한다. 이미 발행한 기사는 개별 편집 기록으로 남는다.
