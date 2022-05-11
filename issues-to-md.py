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


def convert_issue_to_filename(issue):
    title = re.sub('[^A-Za-z0-9. ]+', '', issue.title)
    title = title.replace(' ', '-')
    filename = f"{issue.number}-{title}.md"
    return filename


def rewrite_internal_links(body, output_info):
    url = re.escape('https://github.com/sourmash-bio/sourmash-examples/issues/')
    pattern = f"{url}(\\d+)"

    # find and rewrite all internal links:
    m = re.search(pattern, body)
    while m:
        match_num = m.groups()[0]
        match_num = int(match_num)
        
        match_info = output_info[match_num]
        link = "[{output_title}]({output_filename})".format(**match_info)
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
    labels_by_name = {}
    output_info = defaultdict(dict)

    # build output info, rewrite title, organize issues.
    for issue in issues_list:
        output_filename = convert_issue_to_filename(issue)
        output_title = f"Example {issue.number}: {issue.title}"

        d = dict(output_filename=output_filename, output_title=output_title)
        output_info[issue.number] = d

        for label in issue.labels:
            labels_to_issue[label.name].append(issue)
            labels_by_name[label.name] = label # duplicative but whatevs

    # now, actually do output.
    for issue in issues_list:
        filename = output_info[issue.number]['output_filename']
        output_title = output_info[issue.number]['output_title']

        body = rewrite_internal_links(issue.body, output_info)
        with open("docs/" + filename, "wt") as fp:
            fp.write('# {output_title}'.format(output_title=output_title))
            fp.write("\n\n")
            fp.write(body)
        print(f'wrote to {filename}')

    ### make mkdocs.yml

    all_pages = []
    issues_list.sort(key = lambda x: x.number)
    for issue in issues_list:
        filename = output_info[issue.number]['output_filename']
        title = f"Example {issue.number}: {issue.title}"

        d = {}
        d[title] = filename

        all_pages.append(d)

    all_labels = []
    for label_name, issues_xx in labels_to_issue.items():
        label = labels_by_name[label_name]

        label_filename = f'l-{label}.md'
        with open('docs/' + label_filename, "wt") as fp:
            print(f"# {label.description or label.name}", file=fp)
            for issue in issues_xx:
                fp.write(f"""

[Example {issue.number} - {issue.title}]({output_info[issue.number]['output_filename']})
            
""")

        d = {}
        label_title = label.description or label.name
        d[label_title] = label_filename
        all_labels.append(d)

    all_labels.sort(key = lambda x: list(x.keys())[0])

    nav_contents = []
    nav_contents.append(dict(Home='index.md'))
    nav_contents.append(dict(Examples=all_pages))
    nav_contents.append(dict(Labels=all_labels))

    with open('mkdocs.yml', 'wt') as fp:
        print(mkdocs_yml.format(nav=yaml.safe_dump(nav_contents)), file=fp)

    print("built mkdocs.yml")

    ### make examples.md

    issues_list.sort(key=lambda x: x.number)
    with open('docs/index.md', 'wt') as fp:
        fp.write("# Welcome to sourmash-examples!")
        for issue in issues_list:
            output_filename = output_info[issue.number]['output_filename']
            fp.write(f"""

[Example {issue.number} - {issue.title}]({output_filename})
            
""")

    print("built examples.md")

    return 0


if __name__ == '__main__':
    sys.exit(main())
