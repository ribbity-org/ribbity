#! /usr/bin/env python
"""
Dump a bunch of issues from github into a pickle file.
"""
import sys
import os
import time
from pickle import dump

import tomli

from github import Github
from ribbity import objects


def main(configfile):
    # load config
    with open(configfile, "rb") as fp:
        config_d = tomli.load(fp)

    github_repo = config_d['github_repo']
    issues_dump = config_d['issues_dump']
        

    github_username = config_d.get('github_username')
    if github_username:
        auth_token = os.environ.get('RIBBITY_GH_TOKEN')
        if auth_token:
            print(f"Using github username {github_username} with auth token from RIBBITY_GH_TOKEN", file=sys.stderr)
            g = Github(github_username, auth_token)
        else:
            print("No auth token set with RIBBITY_GH_TOKEN; not using github login for API.", file=sys.stderr)
            g = Github()

    else:
        print("Not using github login for API. You can set 'github_username' in config if you like.", file=sys.stderr)
        g = Github()

    repo = g.get_repo(github_repo)
    print(repo)

    issues_list = []
    for n, issue in enumerate(repo.get_issues()):
        print(f"loading issue {issue.number}...")
        if issue.pull_request:
            print('...issue is a PR. skipping!')
            continue

        if not github_username and n and n % 3:
            time.sleep(1)
        elif n and n % 10:
            time.sleep(1)

        labels = []
        for label in issue.get_labels():
            label_obj = objects.Label(label.color, label.description,
                                      label.name)
            labels.append(label_obj)

        issue_obj = objects.Issue(issue.number,
                                  issue.title,
                                  issue.body,
                                  labels)
        issues_list.append(issue_obj)

    print(f'saving to {issues_dump}')
    with open(issues_dump, 'wb') as fp:
        dump(issues_list, fp)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
