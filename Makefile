all: build

pull:
	ribbity pull site-config.toml

build:
	ribbity build

serve:
	mkdocs serve

deploy:
	mkdocs gh-deploy

test:
	ribbity pull config-test.toml
	ribbity build config-test.toml
	py.test tests
