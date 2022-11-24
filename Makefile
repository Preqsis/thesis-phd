LATEX_FILENAME=thesis
LATEX_EXTENSION=tex

all:
	$(MAKE) build
	$(MAKE) bib
	$(MAKE) build

bib:
	$(BIBER) ./$(LATEX_FILENAME)

build:
	$(PDFLATEX) $(LATEX_FILENAME).$(LATEX_EXTENSION)




