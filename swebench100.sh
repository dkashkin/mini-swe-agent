mini-extra swebench \
--subset verified \
--split test \
--model "vertex_ai/gemini-2.5-pro" \
--workers 20 \
--slice "0:100" \
--environment-class docker \
--output "~/miniout" \
--redo-existing
