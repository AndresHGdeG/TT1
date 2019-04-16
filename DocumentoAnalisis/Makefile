all:	
	
	pdflatex ClasificadorDeNoticias.tex
	bibtex ClasificadorDeNoticias.aux
	pdflatex ClasificadorDeNoticias.tex
	pdflatex ClasificadorDeNoticias.tex
	
	latexmk -c
	rm -r ClasificadorDeNoticias.bbl
