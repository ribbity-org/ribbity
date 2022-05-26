"Test some alternative ribbity config options."
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
        shutil.copy(path_to('test-files', 'config-test-alt-site.toml'),
                    _testdir)
        shutil.copytree(path_to('test-files', 'site-templates.test'),
                        os.path.join(_testdir,
                                     'tests',
                                     'test-files',
                                     'site-templates.test'))

        cwd = os.getcwd()
        os.chdir(_testdir)

        print(f'running ribbity.main_build.main')
        retval = main_build('config-test-alt-site.toml')
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
    with open(path_to(_testdir, 'docsdocs', filename), 'rt') as fp:
        md = fp.read()

    md = md.lstrip()

    return md

### tests!


def test_markdown_issue1():
    # look at issue1 markdown output
    md = load_md('1-test-issue-number-1.md')
    assert md.startswith('# IssuePrefix: test issue number 1')
    assert 'this is a test' in md

    assert '[ribbity-org/ribbity-test-repo#1](https://github.com/ribbity-org/ribbity-test-repo/issues/1)' in md


def test_markdown_issue3():
    # look at issue3 markdown output - unexceptional stuff.
    md = load_md('3-test-toml-config.md')
    assert md.startswith('# IssuePrefix: test TOML config')
    assert 'this example should show up front page' in md

    assert '*[ribbity-org/ribbity-test-repo#3](https://github.com/ribbity-org/ribbity-test-repo/issues/3)*' in md


def test_markdown_issue6():
    # look at issue6 markdown output - do titles get rendered properly?
    md = load_md('6-test-other-things.md')
    assert md.startswith('# IssuePrefix: test `other` things!')

    assert '## Categories' not in md


def test_markdown_index_title():
    index_md = load_md('index.md')
    print(index_md)
    assert index_md.startswith('# Welcome to the ribbity test site!')


def test_markdown_index_examples():
    # look at front page and examples
    index_md = load_md('index.md')
    examples_md = load_md('examples.md')

    # issue 1 only in full list
    assert '[IssuePrefix: test issue number 1](1-test-issue-number-1.md)' not in index_md
    assert '[IssuePrefix: test issue number 1](1-test-issue-number-1.md)' in examples_md

    # issue 3 in both
    assert '[IssuePrefix: test TOML config](3-test-toml-config.md)' in index_md
    assert '[IssuePrefix: test TOML config](3-test-toml-config.md)' in examples_md

    # issue 6 only in full list
    assert '[IssuePrefix: test `other` things!](6-test-other-things.md)' not in index_md
    assert '[IssuePrefix: test `other` things!](6-test-other-things.md)' in examples_md

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

    assert "is [IssuePrefix: issue with labels!](7-issue-with-labels.md)" in md


def test_extra_page():
    # look at a-page.md
    md = load_md('a-page.md')
    assert md.startswith("# a nifty test page!!")
    assert "this page is an extra page." in md

    assert "first issue title: test TOML config" in md




def test_rmdir():
    # test that main_build builds a clean docs dir, in alt site config

    # create FOO.txt in docsdocs/
    newfilename = os.path.join(_testdir, 'docsdocs', 'FOO.txt')
    with open(newfilename, 'wt') as fp:
        print('hello, world', file=fp)

    # build again
    retval = main_build('config-test-alt-site.toml')
    assert retval == 0

    # check - is 'newfilename' there?
    assert not os.path.exists(newfilename)
