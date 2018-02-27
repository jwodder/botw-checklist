checklist.pdf : checklist.tex
	pdflatex checklist.tex
	pdflatex checklist.tex

checklist.tex : mklist.py checklist.json
	python3 mklist.py

clean :
	rm -rf *.aux *.log checklist.tex
