LATEX_FILENAME=thesis
LATEX_EXTENSION=tex

# MAKE, BIBER and PDFLATEX defined in .env file

all:
	$(MAKE) bib
	$(MAKE) build

bib:
	$(BIBER) ./$(LATEX_FILENAME)

build:
	$(PDFLATEX) $(LATEX_FILENAME).$(LATEX_EXTENSION)




