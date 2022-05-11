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

    labels_to_issue = defaultdict(list)
    issues_by_number = {}

    # organize issues and labels
    for issue in issues_list:
        issues_by_number[issue.number] = issue
        print(issue.config)

        for label in issue.labels:
            labels_to_issue[label].append(issue)

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

    all_pages = []
    issues_list.sort(key = lambda x: x.number)
    for issue in issues_list:
        filename = issue.output_filename
        title = issue.output_title
        all_pages.append(dict(title=filename))

    all_labels = []
    for label, issues_for_label in labels_to_issue.items():

        label_filename = label.output_filename
        with open('docs/' + label_filename, "wt") as fp:
            print(f"# {label.output_name}", file=fp)
            for issue in issues_for_label:
                fp.write(f"""

[{issue.output_title}]({issue.output_filename})
            
""")

        d = {}
        label_title = label.description or label.name
        d[label_title] = label_filename
        all_labels.append(d)

    all_labels.sort(key = lambda x: list(x.keys())[0])

    nav_contents = []
    nav_contents.append(dict(Home='index.md'))
    nav_contents.append(dict(Examples=all_pages))
    nav_contents.append(dict(Categories=all_labels))

    with open('mkdocs.yml', 'wt') as fp:
        print(mkdocs_yml.format(nav=yaml.safe_dump(nav_contents)), file=fp)

    print("built mkdocs.yml")

    ### make examples.md

    issues_list.sort(key=lambda x: x.number)
    with open('docs/index.md', 'wt') as fp:
        fp.write("# Welcome to sourmash-examples!")
        for issue in issues_list:
            fp.write(f"""

[Example - {issue.title}]({issue.output_filename})
            
""")

    print("built examples.md")

    return 0


if __name__ == '__main__':
    sys.exit(main())
