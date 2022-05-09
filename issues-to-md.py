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


def convert_issue_to_filename(number, title):
    title = re.sub('[^A-Za-z0-9. ]+', '', title)
    title = title.replace(' ', '-')
    filename = f"{number}-{title}.md"
    return filename


def rewrite_internal_links(body, issues_list):
    url = re.escape('https://github.com/sourmash-bio/sourmash-examples/issues/')
    pattern = f"{url}(\\d+)"

    def get_issue(num):
        num = int(num)
        for x in issues_list:
            if x['n'] == num:
                return x

        assert 0

    # find and rewrite all internal links:
    m = re.search(pattern, body)
    while m:
        match_num = m.groups()[0]
        
        match_issue = get_issue(match_num)
        link = "[{output_title}]({output_filename})".format(**match_issue)
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

    issues_by_number = {}
    labels_to_issue = defaultdict(list)

    for issue_d in issues_list:
        number, title, body = issue_d['n'], issue_d['title'], issue_d['body']
        filename = convert_issue_to_filename(number, title)
        issue_d['output_filename'] = filename
        issue_d['output_title'] = f"Example {number}: {title}"
        issues_by_number[number] = issue_d

        for label in issue_d['labels']:
            labels_to_issue[label].append(issue_d)

    for issue_d in issues_list:
        filename = issue_d['output_filename']
        body = rewrite_internal_links(issue_d['body'], issues_list)
        with open("docs/" + filename, "wt") as fp:
            fp.write('# {output_title}'.format(**issue_d))
            fp.write("\n\n")
            fp.write(body)
        print(f'wrote to {filename}')

    ### make mkdocs.yml

    all_pages = []
    issues_list.sort(key = lambda x: x['n'])
    for issue_d in issues_list:
        filename = issue_d['output_filename']
        title = "Example {n}: {title}".format(**issue_d)

        d = {}
        d[title] = filename

        all_pages.append(d)

    all_labels = []
    for label, issues_xx in sorted(labels_to_issue.items()):
        label_filename = f'l-{label}.md'
        with open('docs/' + label_filename, "wt") as fp:
            print(f"# {label}", file=fp)
            for issue_d in issues_xx:
                fp.write("""

[Example {n} - {title}]({output_filename})
            
""".format(**issue_d))

        d = {}
        d[label] = label_filename
        all_labels.append(d)

    nav_contents = []
    nav_contents.append(dict(Home='index.md'))
    nav_contents.append(dict(Examples=all_pages))
    nav_contents.append(dict(Labels=all_labels))

    with open('mkdocs.yml', 'wt') as fp:
        print(mkdocs_yml.format(nav=yaml.safe_dump(nav_contents)), file=fp)

    print("built mkdocs.yml")

    ### make examples.md

    issues_list.sort(key=lambda x: x['n'])
    with open('docs/index.md', 'wt') as fp:
        fp.write("# Welcome to sourmash-examples!")
        for issue_d in issues_list:
            fp.write("""

[Example {n} - {title}]({output_filename})
            
""".format(**issue_d))

    print("built examples.md")

    return 0


if __name__ == '__main__':
    sys.exit(main())
