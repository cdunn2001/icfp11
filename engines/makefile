LTG ?= ../ltg -print-fields false #-silent true

# The following does not seem to work:
#-print-fields false


run-py:
	${LTG} match ./run.sh ./run.py
run-sh:
	${LTG} match ./run.sh ./run.sh
simple-py:
	${LTG} match ./simple.sh ./simple.py 2>| simple-py
simple-sh:
	${LTG} match ./simple.sh ./simple.sh 2>| simple-sh
dec-py:
	${LTG} match ./run.sh decspread.py 2>| dec-py
t:
	-./ltg.py match ./run.sh ./decspread.py 2>&1 >| t
q:
	${LTG} match ./run.sh ./decspread.py
.PHONY: t q
