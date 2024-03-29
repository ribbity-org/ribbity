all: build

pull:
	ribbity pull site-config.toml

build:
	ribbity build

serve:
	mkdocs serve

pulltest:
	ribbity pull config-test.toml
	py.test tests

test:
	py.test tests

update_output:
	ribbity build output_docs/config-test.toml
	ribbity build output_docs/config-alt.toml
	git add output_docs/test-site output_docs/alt-test-site
