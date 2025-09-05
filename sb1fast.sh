mkdir -p out && 
zip -rq out_backup_$(date +%m%d%y_%H%M).zip out && 
rm -rf out/* &&
mini-extra swebench \
--subset verified \
--split test \
--model "vertex_ai/gemini-2.5-pro" \
--workers 1 \
--filter "scikit-learn__scikit-learn-13135" \
--environment-class docker \
--output "out" \
--redo-existing \
--run-id "$1"