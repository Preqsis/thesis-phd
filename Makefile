LATEX_FILENAME=thesis
LATEX_EXTENSION=tex
SHELL=/bin/zsh

# MAKE, BIBER and PDFLATEX defined in .env file

all:
	$(MAKE) bib
	$(MAKE) build

bib:
	$(BIBER) ./$(LATEX_FILENAME)

build:
	$(PDFLATEX) $(LATEX_FILENAME).$(LATEX_EXTENSION)

# builds chapters into separate files
sep:
	$(PDFLATEX) -jobname=ch1 "\includeonly{chapters/multilayer_dripping_handrail.tex}\input{thesis.tex}"



