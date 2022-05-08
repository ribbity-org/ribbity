rule all:
    input:
        "sourmash-examples.dmp",
        "mkdocs.yml"

rule dump_issues:
    input:
        "dump-issues.py"
    output:
        "sourmash-examples.dmp"
    shell: """
        python dump-issues.py sourmash-bio/sourmash-examples -o {output}
    """
        
rule make_markdown:
    input:
        dmp = "sourmash-examples.dmp",
        script = "issues-to-md.py"
    output:
        "mkdocs.yml",
        "docs/examples.md"
    shell: """
        ./issues-to-md.py {input.dmp}
    """
