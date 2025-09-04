mini-extra swebench \
--model claude-sonnet-4-20250514 \
--subset verified \
--split test \
--model "gemini/gemini-2.5-pro" \
--workers 1 \
--slice "0:1" \
--environment-class docker \
--output "~/miniout"
