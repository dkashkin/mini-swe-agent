mini-extra swebench \
--subset verified \
--split test \
--model "vertex_ai/gemini-2.5-pro" \
--workers 100 \
--environment-class docker \
--output "/home/jupyter/miniout" \
--redo-existing