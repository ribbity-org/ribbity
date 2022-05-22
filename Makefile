all: build

pull:
	ribbity pull site-config.toml

build:
	ribbity build

serve:
	mkdocs serve

pulltest:
	ribbity pull config-test.toml
	ribbity build config-test.toml
	py.test tests

test:
	ribbity build config-test.toml
	py.test tests
