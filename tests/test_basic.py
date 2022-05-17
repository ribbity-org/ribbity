"Basic tests of ribbity functionality."

from pickle import load, dump
import os

import pytest

thisdir = os.path.dirname(os.path.abspath(__file__))
def path_to(*p):
    return os.path.join(thisdir, *p)


def load_md(filename):
    with open(path_to('../docs', filename), 'rt') as fp:
        md = fp.read()
    return md

def load_dump(filename):
    with open(path_to('..', filename), 'rb') as fp:
        issues_list = load(fp)
    return issues_list


def get_issue_by_number(num):
    issues_list = load_dump('ribbity-test.dmp')
    issue = [ iss for iss in issues_list if iss.number == num][0]
    return issue


def test_pull_issue1_basic():
    # test object contents for issue 1
    issue = get_issue_by_number(1)

    assert issue.number == 1
    assert issue.title == 'test issue number 1'
    assert 'this is a test!' in issue.body, (issue.body,)
    assert not issue.labels
    assert issue.output_title == 'Example: test issue number 1'
    assert issue.output_filename == '1-test-issue-number-1.md'
    assert issue.index_title == 'Example: test issue number 1'

    # properly parsed TOML?
    assert len(issue.config) == 2
    assert 'frontpage' in issue.config
    assert 'priority' in issue.config

    # properly represented in issue object?
    assert not issue.is_frontpage
    assert issue.priority == 999


def test_pull_issue2_no_such_issue():
    # issue 2 is closed and should not show up
    with pytest.raises(IndexError):
        issue = get_issue_by_number(2)


def test_pull_issue4_open_pr():
    # issue 4 is a pr and should not show up
    with pytest.raises(IndexError):
        issue = get_issue_by_number(4)
