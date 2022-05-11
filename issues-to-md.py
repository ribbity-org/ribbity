#! /usr/bin/env python
"""
Convert an issues dump file (from dump-issues.py) into a mkdocs site.
"""
import sys
import argparse
import re
from pickle import load
import yaml
from collections import defaultdict


def rewrite_internal_links(body, issues_by_number):
    url = re.escape('https://github.com/sourmash-bio/sourmash-examples/issues/')
    pattern = f"{url}(\\d+)"

    # find and rewrite all internal links:
    m = re.search(pattern, body)
    while m:
        match_num = m.groups()[0]
        match_num = int(match_num)
        match_issue = issues_by_number[match_num]
        
        link = f"[{match_issue.output_title}]({match_issue.output_filename})"
        body = body[:m.start()] + link + body[m.end():]
        m = re.search(pattern, body)

    return body


mkdocs_yml = """\
site_name: sourmash examples
site_url: https://ctb.github.io/ribbity/

theme:
  logo: assets/sourmash-logo.png
  favicon: assets/sourmash.ico
  name: ivory

nav:
{nav}
"""


def main():
    p = argparse.ArgumentParser()
    p.add_argument('issues_dmp')
    args = p.parse_args()

    with open(args.issues_dmp, 'rb') as fp:
        issues_list = load(fp)

    print(f"loaded {len(issues_list)} issues from '{args.issues_dmp}'")

    labels_to_issues = defaultdict(list)
    issues_by_number = {}

    # organize issues and labels
    for issue in issues_list:
        issues_by_number[issue.number] = issue
        if issue.config:
            print(issue.config)

        for label in issue.labels:
            labels_to_issues[label].append(issue)

    # now, actually do output.
    for issue in issues_list:
        filename = issue.output_filename

        body = rewrite_internal_links(issue.body, issues_by_number)
        with open("docs/" + filename, "wt") as fp:
            print(f"""\
# {issue.output_title}

*[sourmash-bio/sourmash-examples#{issue.number}](https://github.com/sourmash-bio/sourmash-examples/issues/{issue.number})*

---

{body}
""", file=fp)
        print(f'wrote to {filename}')

    ### make mkdocs.yml

    # build a list of all pages
    all_examples = []
    issues_list.sort()
    for issue in issues_list:
        print(f'... issue #{issue.number}')
        filename = issue.output_filename
        title = issue.index_title
        all_examples.append({ title: filename })

    # build a list of all labels
    all_labels = []
    for label, issues_for_label in labels_to_issues.items():
        label_filename = label.output_filename
        with open('docs/' + label_filename, "wt") as fp:
            print(f"# {label.output_name}", file=fp)
            for issue in sorted(issues_for_label):
                fp.write(f"""\

[{issue.output_title}]({issue.output_filename})
            
""")

        d = {}
        label_title = label.description or label.name
        d[label_title] = label_filename
        all_labels.append(d)

    all_labels.sort(key = lambda x: list(x.keys())[0])

    nav_contents = []
    nav_contents.append(dict(Home='index.md'))
    nav_contents.append(dict(Examples=all_examples))
    nav_contents.append(dict(Categories=all_labels))

    with open('mkdocs.yml', 'wt') as fp:
        print(mkdocs_yml.format(nav=yaml.safe_dump(nav_contents)), file=fp)

    print("built mkdocs.yml")

    ### make index.md

    issues_list.sort()
    with open('docs/index.md', 'wt') as fp:
        print(f"""\
# Welcome to sourmash-examples!

This is a collection of examples and recipes for [the sourmash
software](https://sourmash.readthedocs.io/), for fast genomic and
metagenomic sequencing data analysis.

sourmash can quickly search genomes and metagenomes for matches; see
[our list of available search
databases](https://sourmash.readthedocs.io/en/latest/databases.html).

sourmash also supports taxonomic exploration and classification
for genomes and metagenomes with the NCBI and
[GTDB](https://gtdb.ecogenomic.org/) taxonomies.

The paper [Large-scale sequence comparisons with sourmash (Pierce et
al., 2019)](https://f1000research.com/articles/8-1006) gives an
overview of what sourmash does and how sourmash works.

Do you have questions or comments? [File an
issue](https://github.com/sourmash-bio/sourmash/issues) or [come chat
on gitter](https://gitter.im/sourmash-bio/community)!

---

*Go to: [All examples](examples.md) | [All categories](labels.md)*

## Start here!

""", file=fp)
        for issue in issues_list:
            if issue.config.get('frontpage'):
                print(f"""
[Example: {issue.title}]({issue.output_filename})
""", file=fp)

    print("built index.md")

    ### make examples.md

    issues_list.sort()
    with open('docs/examples.md', 'wt') as fp:
        print("""\
# All examples

*Go to: [Home](index.md) | [All categories](labels.md)*

---
""", file=fp)
        for issue in issues_list:
            print(f"""
[Example: {issue.title}]({issue.output_filename})
""", file=fp)

    print("built examples.md")

    ### make labels.md

    with open('docs/labels.md', 'wt') as fp:
        print("""\
# All categories

*Go to: [Home](index.md) | [All examples](examples.md)*

---

""", file=fp)
        for label in labels_to_issues:
            print(f"""
[{label.description} - {len(labels_to_issues[label])} examples]({label.output_filename})
""", file=fp)

    print("built labels.md")

    return 0


if __name__ == '__main__':
    sys.exit(main())
