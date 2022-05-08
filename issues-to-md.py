#! /usr/bin/env python
import sys
import argparse
import pprint
import re
import os
import time
from pickle import load
import yaml

from github import Github

def convert_issue_to_filename(number, title):
    title = re.sub('[^A-Za-z0-9. ]+', '', title)
    title = title.replace(' ', '-')
    filename = f"{number}-{title}.md"
    return filename


mkdocs_yml = """\
site_name: My Docs

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

    for issue_d in issues_list:
        number, title, body = issue_d['n'], issue_d['title'], issue_d['body']
        filename = convert_issue_to_filename(number, title)
        with open("docs/" + filename, "wt") as fp:
            fp.write(f'# Example {number}: {title}')
            fp.write("\n\n")
            fp.write(body)
        print(f'wrote to {filename}')

        issue_d['output_filename'] = filename

    ### make mkdocs.yml

    all_pages = []
    issues_list.sort(key = lambda x: x['n'])
    for issue_d in issues_list:
        filename = issue_d['output_filename']
        title = "Example {n}: {title}".format(**issue_d)

        d = {}
        d[title] = filename

        all_pages.append(d)

    nav_contents = []
    nav_contents.append(dict(Home='index.md'))
    nav_contents.append(dict(Examples=all_pages))

    with open('mkdocs.yml', 'wt') as fp:
        print(mkdocs_yml.format(nav=yaml.safe_dump(nav_contents)), file=fp)

    print("built mkdocs.yml")

    ### make examples.md

    issues_list.sort(key=lambda x: x['n'])
    with open('docs/examples.md', 'wt') as fp:
        fp.write("# All examples")
        for issue_d in issues_list:
            fp.write("""

[Example {n} - {title}]({output_filename})
            
""".format(**issue_d))

    print("built examples.md")

    return 0


if __name__ == '__main__':
    sys.exit(main())
