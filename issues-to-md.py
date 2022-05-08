#! /usr/bin/env python
import sys
import argparse
import pprint
import re
import os
import time

from github import Github

def convert_issue_to_filename(issue):
    title = re.sub('[^A-Za-z0-9. ]+', '', issue.title)
    title = title.replace(' ', '-')
    filename = f"{issue.number}-{title}.md"
    return filename


def main():
    p = argparse.ArgumentParser()
    p.add_argument('repo')
    args = p.parse_args()

    g = Github()
    repo = g.get_repo('sourmash-bio/sourmash-examples')
    print(repo)
    print(list(repo.get_issues()))

    for n, issue in enumerate(repo.get_issues()):
        if n and n % 3:
            time.sleep(1)

        filename = 'docs/' + convert_issue_to_filename(issue)
        with open(filename, "wt") as fp:
            fp.write(f'# Example {issue.number}: {issue.title}')
            fp.write("\n\n")
            fp.write(issue.body)
        print(f'wrote to {filename}')
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
