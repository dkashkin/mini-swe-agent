mini-extra swebench \
--model claude-sonnet-4-20250514 \
--subset verified \
--split test \
--model "gemini/gemini-2.5-pro" \
--workers 1 \
--filter "sympy__sympy-24443" \
--environment-class docker \
--output "/home/jupyter/miniout" \
--redo-existing 
