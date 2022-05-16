all:
	ribbity build

pull:
	ribbity pull site-config.toml

serve:
	mkdocs serve

deploy:
	mkdocs gh-deploy
