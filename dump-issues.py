#! /usr/bin/env python
import sys
import argparse
import pprint
import re
import os
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

        issues_list.append(dict(n=issue.number,
                                title=issue.title,
                                body=issue.body))

    print(f'saving to {args.output}')
    with open(args.output, 'wb') as fp:
        dump(issues_list, fp)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
