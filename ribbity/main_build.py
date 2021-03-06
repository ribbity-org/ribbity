#! /usr/bin/env python
"""
Convert an issues dump file (from dump-issues.py) into a mkdocs site.
"""
import sys
import contextlib
import os
from pickle import load
import yaml
from collections import defaultdict
import shutil

from ribbity.render import Piggy
from ribbity.version import version
from ribbity.config import RibbityConfig
from ribbity.parse_md import rewrite_issue_body
from ribbity import objects


def main(configfile):
    # load config
    config = RibbityConfig.load(configfile)

    print(f"== ribbity v{version} build - config file {configfile} ==\n",
          file=sys.stderr)

    github_repo = config.github_repo
    assert not github_repo.startswith('http')
    github_repo = github_repo.strip('/')

    issues_dump = config.issues_dump

    with open(issues_dump, 'rb') as fp:
        issues_list = load(fp)

    print(f"loaded {len(issues_list)} issues from '{issues_dump}'")

    #
    # handle include_only labels
    #
    if config.include_only_labels:
        include_labels = set(config.include_only_labels)
        new_issues_list = []

        # every issue must include at least one include label.
        for ix in issues_list:
            ix_labels = set(( l.name for l in ix.labels ))
            if include_labels & ix_labels:
                new_issues_list.append(ix)

        if len(new_issues_list) != issues_list:
            print(f"removed {len(issues_list) - len(new_issues_list)} issues because of include_only labels",
                  file=sys.stderr)
            issues_list = new_issues_list

    #
    # handle ignored - if individual page config is set to 'ignore'.
    #
    new_issues_list = [ ix for ix in issues_list if not ix.is_ignored ]
    if len(new_issues_list) != issues_list:
        print(f"ignored {len(issues_list) - len(new_issues_list)} issues because 'ignore = true' was set",
              file=sys.stderr)
        issues_list = new_issues_list

    #
    # handle exclude_labels
    #
    if config.exclude_labels:
        exclude_labels = set(config.exclude_labels)
        new_issues_list = []

        # if an issue has one or more of the exclusion labels, exclude!
        for ix in issues_list:
            ix_labels = set(( l.name for l in ix.labels ))
            if not exclude_labels & ix_labels:
                new_issues_list.append(ix)

        if len(new_issues_list) != issues_list:
            print(f"excluded {len(issues_list) - len(new_issues_list)} issues because of excluded labels",
                  file=sys.stderr)
            issues_list = new_issues_list


    del new_issues_list

    with contextlib.suppress(FileNotFoundError):
        shutil.rmtree(config.docs_dir)
        print(f"removed existing '{config.docs_dir}' subdirectory", file=sys.stderr)

    os.mkdir(config.docs_dir)
    print(f"created '{config.docs_dir}' subdirectory", file=sys.stderr)

    # remove ignore_labels
    ignore_labels = set(config.ignore_labels)
    new_issues_list = []
    for ix in issues_list:
        issue_labels = [ xx for xx in ix.labels if xx.name not in ignore_labels ]
        if issue_labels != ix.labels:
            new_ix = objects.Issue(ix.number, ix.title, ix.body, issue_labels)
            new_issues_list.append(new_ix)
        else:
            new_issues_list.append(ix)
    issues_list = new_issues_list

    # organize issues and labels
    labels_to_issues = defaultdict(list)
    issues_by_number = {}

    ignore_labels = set(config.ignore_labels)
    for issue in issues_list:
        issues_by_number[issue.number] = issue
        for label in issue.labels:
            if label.name not in ignore_labels:
                labels_to_issues[label].append(issue)

    # build piggy object
    piggy_obj = Piggy(issues_list, labels_to_issues, config)

    # now, output all issues:
    for issue in issues_list:
        filename = issue.output_filename

        body = issue.body
        if body is None:
            body = ''

        body = rewrite_issue_body(body, issues_by_number, config)

        filepath = os.path.join(config.docs_dir, filename)
        with open(filepath, "wt") as fp:
            md = piggy_obj.render("_generic_issue.md", issue=issue, body=body)
            fp.write(md)
        print(f'wrote to {filepath}', end='\r\033[K', file=sys.stderr)

    # output all labels:
    for label, issues_for_label in labels_to_issues.items():
        label_filename = os.path.join(config.docs_dir, label.output_filename)
        with open(label_filename, "wt") as fp:
            md = piggy_obj.render("_generic_label.md",
                                  label=label,
                                  issues_for_label=issues_for_label)
            fp.write(md)
        print(f"wrote to {label_filename}", end='\r\033[K', file=sys.stderr)

    ### make mkdocs.yml
    nav_contents = []
    nav_contents.append(dict(Home='index.md'))
    nav_contents.append({'All examples': 'examples.md'})
    nav_contents.append({'All categories': 'labels.md'})

    ## write mkdocs.yml
    mkdocs_config = [dict(site_name=config.site_name),
                     dict(site_url=config.site_url),
                     dict(nav=nav_contents),
                     dict(use_directory_urls=False),
                     dict(docs_dir=config.docs_dir),
                     dict(site_dir=config.site_dir)]
    with open('mkdocs.yml', 'wt') as fp:
        for element in mkdocs_config:
            print(yaml.safe_dump(element), file=fp)
    print("wrote mkdocs.yml", file=sys.stderr, end='\r\033[K')

    ## set up variable dict for rendering
    issues_list.sort()
    render_variables = dict(issues_list=issues_list,
                            labels_to_issues=labels_to_issues,
                            piggy=piggy_obj)

    ### render the pages explicitly requested
    for filename in config.add_pages:
        # load from ./pages/ and render with jinja2
        md = piggy_obj.render(filename, **render_variables)

        # save to docs dir
        filepath = os.path.join(config.docs_dir, filename)
        with open(filepath, "wt") as fp:
            fp.write(md)
        print(f"built {filepath}", file=sys.stderr, end='\r\033[K')

    print("\nribbity is done!", file=sys.stderr)

    return 0


if __name__ == '__main__':
    sys.exit(main())
