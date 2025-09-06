mini-extra swebench \
--subset verified \
--split test \
--model "vertex_ai/gemini-2.5-pro" \
--workers 30 \
--environment-class docker \
--output "out" \
--run-id "$1" \
--shuffle