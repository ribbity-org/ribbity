import tomli

toml_config = 'site-config.toml'

with open(toml_config, 'rb') as fp:
    config_d = tomli.load(fp)

github_repo = config_d['github_repo']
issues_dump = config_d['issues_dump']

rule all:
    input:
        "sourmash-examples.dmp",
        "mkdocs.yml",
        "docs/index.md"

rule dump_issues:
    output:
        issues_dump
    shell: """
        python -m ribbity pull {toml_config}
    """
        
rule make_markdown:
    input:
        dmp = issues_dump,
    output:
        "mkdocs.yml",
        "docs/index.md"
    shell: """
        rm -f docs/* || true
        python -m ribbity build {toml_config}
    """
