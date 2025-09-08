mkdir -p out && 
zip -rq out_backup_$(date +%m%d%y_%H%M).zip out && 
rm -rf out/* &&
mini-extra swebench \
--subset verified \
--split test \
--model "vertex_ai/claude-sonnet-4@20250514" \
--workers 1 \
--filter "astropy__astropy-7166" \
--environment-class docker \
--output "out" \
--redo-existing \
--run-id "$1"