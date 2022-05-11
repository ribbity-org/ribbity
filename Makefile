all:
	snakemake -j 1

force:
	touch issues-to-md.py
	snakemake -j 1

serve:
	mkdocs serve

deploy:
	mkdocs gh-deploy
