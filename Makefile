all:
	snakemake -j 1

serve:
	mkdocs serve

deploy:
	mkdocs gh-deploy
