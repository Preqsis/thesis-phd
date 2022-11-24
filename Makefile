FILENAME=thesis

all:
	make build
	make bib
	make build
	make split

bib:
	biber ./$(FILENAME)

build:
	pdflatex $(FILENAME).tex

split:
	python ./python/split_by_chapters.py --infile ./$(FILENAME).pdf --outdir ./splits

clean:
	find . -type f ! -path "./.git/*" ! -path "./img/*" ! -path "./.*" ! -path "./python/*" ! -path "./misc/*" ! -path "./logo/*" ! -name "Makefile" ! -name "*.tex" ! -name "*.cls" ! -name "*.bib" ! -name "*.md" ! -name "*.sty" -exec rm -vf {} +
	


