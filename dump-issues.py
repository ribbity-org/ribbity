#! /usr/bin/env python
"""
Dump a bunch of issues from github into a pickle file.
"""
import sys
import argparse
import time
from pickle import dump

from github import Github
from ribbity import objects


def main():
    p = argparse.ArgumentParser()
    p.add_argument('repo')
    p.add_argument('-o', '--output', required=True)
    args = p.parse_args()

    g = Github()
    repo = g.get_repo(args.repo)
    print(repo)

    issues_list = []
    for n, issue in enumerate(repo.get_issues()):
        print(f"loading issue {issue.number}...")
        if n and n % 3:
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

    print(f'saving to {args.output}')
    with open(args.output, 'wb') as fp:
        dump(issues_list, fp)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
