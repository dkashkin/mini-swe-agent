mkdir -p out && 
zip -rq out_backup_$(date +%m%d%y_%H%M).zip out && 
rm -rf out/* &&
mini-extra swebench \
--subset verified \
--split test \
--model "vertex_ai/gemini-2.5-pro" \
--workers 20 \
--filter "^(astropy__astropy-13033|astropy__astropy-14096|astropy__astropy-14309|astropy__astropy-14539|astropy__astropy-14598|astropy__astropy-14995|django__django-11087|django__django-11728|django__django-13794|django__django-14011|django__django-14376|django__django-16136|django__django-16667|matplotlib__matplotlib-20676|matplotlib__matplotlib-23314|matplotlib__matplotlib-24570|matplotlib__matplotlib-25479|matplotlib__matplotlib-25960|pydata__xarray-6744|sympy__sympy-14976)$" \
--environment-class docker \
--output "out" \
--redo-existing \
--run-id "$1"