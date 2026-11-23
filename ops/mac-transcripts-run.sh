#!/bin/bash
# AI 브리핑: 후보 영상 자막을 받아 비공개 저장소(ai-brief-transcripts)에 올린다. launchd가 매시 50분에 실행.
set -u
cd "$HOME/.ai-brief" || exit 1
echo "== $(date '+%F %T')"
git -C repo pull -q --ff-only || git -C repo reset -q --hard origin/main
git -C transcripts pull -q 2>/dev/null || true
./venv/bin/python repo/collector/mac_transcripts.py repo transcripts
cd transcripts
git add -A
if ! git diff --cached --quiet; then
  git commit -q -m "자막: $(date -u +%FT%H:%MZ)"
  git push -q -u origin HEAD:main || { git pull -q --rebase origin main && git push -q origin HEAD:main; }
fi
