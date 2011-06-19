LTG ?= time ../ltg #-print-fields true #-silent true


# The following does not seem to work:
#-print-fields false
SHELL=bash

run-py:
	${LTG} match ./run.sh ./run.py
run-sh:
	${LTG} match ./run.sh ./run.sh
simple-py:
	${LTG} match ./simple.sh ./simple.py |& tee simple-py.log | tail
simple-sh:
	${LTG} match ./simple.sh ./simple.sh |& tee simple-sh.log | tail
dec-py:
decspread-py:
killatron-py:
%-py:
	${LTG} match ./run.sh ./$*.py |& tee $*-py.log | tail
t:
	-./ltg.py match ./run.sh ./decspread.py 2>&1 >| t
q:
	${LTG} match ./run.sh ./decspread.py
zz:
	./ltg.py match ./run.sh ./zombify.py
z:
	${LTG} match ./run.sh ./zombify.py
s:
	./ltg.py match ./run.sh ./s.py | less
compose:
	(./compose.py; (./compose.py | ../ltg only) 2>&1 | head -10000 | perl -ne 'print if /\d=|Error/') 2>&1 | less

.PHONY: t q z
