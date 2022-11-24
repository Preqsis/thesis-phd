MAINFILE=thesis

all:
	$(MAKE) build
	$(MAKE) bib
	$(MAKE) build

bib:
	$(BIBER) ./$(MAINFILE)

build:
	$(PDFLATEX) $(MAINFILE).tex

split:
	python ./python/split_by_chapters.py --infile ./$(MAINFILE).pdf --outdir ./splits
