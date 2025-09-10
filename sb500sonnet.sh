mkdir -p out && 
zip -rq out_backup_$(date +%m%d%y_%H%M).zip out && 
rm -rf out/* &&
mini-extra swebench \
--subset verified \
--split test \
--model "vertex_ai/claude-sonnet-4" \
--workers 7 \
--environment-class docker \
--output "out" \
--run-id "$1" \
--shuffle