mkdir -p out && 
zip -rq out_backup_$(date +%m%d%y_%H%M).zip out && 
rm -rf out/* &&
mini-extra swebench \
--subset verified \
--split test \
--model "vertex_ai/gemini-2.5-pro" \
--workers 30 \
--slice "0:100" \
--environment-class docker \
--output "out" \
--run-id "$1" \
--redo-existing \
--shuffle