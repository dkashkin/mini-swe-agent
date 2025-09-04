mkdir -p out && 
zip -rq out_backup_$(date +%m%d%y_%H%M).zip out && 
rm -rf out/* &&
mini-extra swebench \
--model "vertex_ai/gemini-2.5-pro" \
--subset verified \
--split test \
--workers 1 \
--filter "django__django-12155" \
--environment-class docker \
--output "/home/jupyter/miniout" \
--redo-existing 