checklist.pdf : checklist.tex
	latexmk -pdf checklist.tex

checklist.tex : mklist.py checklist.json
	python3 mklist.py

clean :
	latexmk -C
	rm -f checklist.tex
