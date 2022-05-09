#! /usr/bin/env python
"""
Dump a bunch of issues from github into a pickle file.
"""
import sys
import argparse
import time
from pickle import dump

from github import Github


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
        if n and n % 3:
            time.sleep(1)

        labels = [ label.name for label in issue.get_labels() ]

        issues_list.append(dict(n=issue.number,
                                title=issue.title,
                                body=issue.body,
                                labels=labels))

    print(f'saving to {args.output}')
    with open(args.output, 'wb') as fp:
        dump(issues_list, fp)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
