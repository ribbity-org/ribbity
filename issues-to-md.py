#! /usr/bin/env python
"""
Convert an issues dump file (from dump-issues.py) into a mkdocs site.
"""
import sys
import argparse
import re
from pickle import load
import yaml
import tomli
from collections import defaultdict

from ribbity.render import render_md


def rewrite_internal_links(body, issues_by_number, github_repo):
    url = re.escape(f'https://github.com/{github_repo}/issues/')
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


def main():
    p = argparse.ArgumentParser()
    p.add_argument('issues_dmp')
    args = p.parse_args()

    # load config
    with open("site-config.toml", "rb") as fp:
        config_d = tomli.load(fp)

    github_repo = config_d['github_repo']
    assert not github_repo.startswith('http')
    github_repo = github_repo.strip('/')

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

    # now, output all issues:
    for issue in issues_list:
        filename = issue.output_filename

        body = rewrite_internal_links(issue.body, issues_by_number, github_repo)
        with open("docs/" + filename, "wt") as fp:
            md = render_md("_generic_issue.md",
                           dict(issue=issue, body=body, **config_d))
            fp.write(md)
        print(f'wrote to {filename}')

    # output all labels:
    all_labels = []
    for label, issues_for_label in labels_to_issues.items():
        label_filename = label.output_filename
        with open('docs/' + label_filename, "wt") as fp:
            md = render_md("_generic_label.md",
                           dict(label=label, issues_for_label=issues_for_label,
                                **config_d))
            fp.write(md)
        print(f"wrote to {label_filename}")

    ### make mkdocs.yml
    nav_contents = []
    nav_contents.append(dict(Home='index.md'))
    nav_contents.append({'All examples': 'examples.md'})
    nav_contents.append({'All categories': 'labels.md'})

    ## write mkdocs.yml
    mkdocs_config = [dict(site_name=config_d['site_name']),
                     dict(site_url=config_d['site_url']),
                     dict(nav=nav_contents)]
    with open('mkdocs.yml', 'wt') as fp:
        for element in mkdocs_config:
            print(yaml.safe_dump(element), file=fp)
    print("wrote mkdocs.yml", file=sys.stderr)

    ## set up variable dict for rendering
    issues_list.sort()
    render_variables = dict(issues_list=issues_list,
                            labels_to_issues=labels_to_issues,
                            **config_d)

    ### render the pages explicitly requested
    for filename in config_d['add_pages']:
        # load from ./pages/ and render with jinja2
        md = render_md(filename, render_variables)

        # save to ./docs/
        with open(f"docs/{filename}", "wt") as fp:
            fp.write(md)
        print(f"built {filename}", file=sys.stderr)

    return 0


if __name__ == '__main__':
    sys.exit(main())
