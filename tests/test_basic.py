"Basic tests of ribbity functionality."
from pickle import load
import os
import tempfile
import shutil

import pytest

from ribbity.main_pull import main as main_pull
from ribbity.main_build import main as main_build

_testdir = None


@pytest.fixture(autouse=True, scope='module')
def module_setup_teardown():
    global _testdir

    with tempfile.TemporaryDirectory(prefix='ribbity_') as _testdir:
        print(f'running tests in temp directory {_testdir}')

        shutil.copy(path_to('..', 'ribbity-test.dmp'), _testdir)
        shutil.copy(path_to('..', 'config-test.toml'), _testdir)

        cwd = os.getcwd()
        os.chdir(_testdir)

        print(f'running ribbity.main_build.main')
        retval = main_build('config-test.toml')
        assert retval == 0

        # run the tests!
        try:
            yield
        finally:
            os.chdir(cwd)

    # teardown here, if anything.
    # note: temp directory should be removed automatically by context mgr.
    print('done with tests!')


thisdir = os.path.dirname(os.path.abspath(__file__))
def path_to(*p):
    return os.path.join(thisdir, *p)


def load_md(filename):
    with open(path_to(_testdir, 'docs', filename), 'rt') as fp:
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


### tests!


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
        get_issue_by_number(2)


def test_pull_issue4_open_pr():
    # issue 4 is a pr and should not show up
    with pytest.raises(IndexError):
        get_issue_by_number(4)


def test_pull_issue5_closed_pr():
    # issue 5 is a pr and should not show up
    with pytest.raises(IndexError):
        get_issue_by_number(5)


def test_pull_issue3_basic():
    # test object contents for issue 3, which has toml config
    issue = get_issue_by_number(3)

    assert issue.number == 3
    assert issue.title == 'test TOML config'
    assert 'this example should show up front' in issue.body, (issue.body,)
    assert not issue.labels
    assert issue.output_title == 'Example: test TOML config'
    assert issue.output_filename == '3-test-toml-config.md'
    assert issue.index_title == 'Example: test TOML config'

    # properly parsed TOML?
    assert len(issue.config) == 2
    assert 'frontpage' in issue.config
    assert 'priority' in issue.config

    # properly represented in issue object?
    assert issue.is_frontpage
    assert issue.priority == 5


def test_pull_issue6_basic_properties():
    # test object contents for issue 6, title/index rewriting and no toml
    issue = get_issue_by_number(6)

    assert issue.number == 6
    assert issue.title == 'test `other` things!'
    assert not issue.labels
    assert issue.output_title == 'Example: test `other` things!'
    assert issue.output_filename == '6-test-other-things.md'
    assert issue.index_title == 'Example: test other things'

    # no TOML?
    assert not issue.config

    # properly represented in issue object with defaults?
    assert not issue.is_frontpage
    assert issue.priority == 999


def test_pull_issue10_basic_properties():
    # test object contents for issue 10, ignored
    issue = get_issue_by_number(10)

    assert issue.number == 10
    assert issue.is_ignored

    assert not os.path.exists(path_to('../docs',
                                      '10-test-ignore-functionality.md'))


def test_markdown_issue1():
    # look at issue1 markdown output
    md = load_md('1-test-issue-number-1.md')
    assert md.startswith('# Example: test issue number 1')
    assert 'this is a test' in md

    assert '[ribbity-org/ribbity-test-repo#1](https://github.com/ribbity-org/ribbity-test-repo/issues/1)' in md


def test_markdown_issue3():
    # look at issue3 markdown output - unexceptional stuff.
    md = load_md('3-test-toml-config.md')
    assert md.startswith('# Example: test TOML config')
    assert 'this example should show up front page' in md

    assert '*[ribbity-org/ribbity-test-repo#3](https://github.com/ribbity-org/ribbity-test-repo/issues/3)*' in md


def test_markdown_issue6():
    # look at issue6 markdown output - do titles get rendered properly?
    md = load_md('6-test-other-things.md')
    assert md.startswith('# Example: test `other` things!')

    assert '## Categories' not in md


def test_markdown_index_examples():
    # look at front page and examples
    index_md = load_md('index.md')
    examples_md = load_md('examples.md')

    # issue 1 only in full list
    assert '[Example: test issue number 1](1-test-issue-number-1.md)' not in index_md
    assert '[Example: test issue number 1](1-test-issue-number-1.md)' in examples_md

    # issue 3 in both
    assert '[Example: test TOML config](3-test-toml-config.md)' in index_md
    assert '[Example: test TOML config](3-test-toml-config.md)' in examples_md

    # issue 6 only in full list
    assert '[Example: test `other` things!](6-test-other-things.md)' not in index_md
    assert '[Example: test `other` things!](6-test-other-things.md)' in examples_md

    # issue 10 not in anything
    assert not '10-test-ignore-functionality.md)' in examples_md


def test_markdown_issue7():
    # look at issue7, with labels
    md = load_md('7-issue-with-labels.md')

    assert '## Categories' in md
    assert '[This issue or pull request already exists](l-duplicate.md)' in md
    assert '[Good for newcomers](l-good first issue.md)' in md

    # check in labels.md @CTB


def test_markdown_issue8():
    # look at issue8, with labels
    md = load_md('8-what-happens-with-external-links.md')

    assert '## Categories' not in md
    assert """in a [markdown link](https://github.com/sourmash-bio/sourmash-examples/issues?q=is%3Aissue+is%3Aopen+%27frontpage%3A+True%27).""" in md

    assert "\n[http://github.com/ribbity-org/ribbity](http://github.com/ribbity-org/ribbity) at beginning" in md
    assert "\n[http://github.com/ribbity-org/ribbity](http://github.com/ribbity-org/ribbity)\n" in md
    assert "\n[https://github.com/ribbity-org/ribbity](https://github.com/ribbity-org/ribbity)\n" in md
    assert "at end: [http://github.com/ribbity-org/ribbity](http://github.com/ribbity-org/ribbity)" in md
    assert 'src="https://user-images.githubusercontent.com/51016' in md


def test_markdown_issue9():
    # look at issue9, with reference to issue 7
    md = load_md('9-this-issue-refers-to-another-issue.md')

    assert "is [Example: issue with labels!](7-issue-with-labels.md)" in md
