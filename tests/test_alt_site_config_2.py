"Test some alternative ribbity config options."
from pickle import load
import os
import tempfile
import shutil

import pytest

from ribbity.main_pull import main as main_pull
from ribbity.main_build import main as main_build

_testdir = None


from test_basic import get_issue_by_number, path_to


#
# this module setup/teardown function establishes a clean environment
# in a temp directory and then builds the ribbity site there.
#
# note: 'config-test-alt-site.toml' builds under docsdocs2/.
#

@pytest.fixture(autouse=True, scope='module')
def module_setup_teardown():
    global _testdir

    with tempfile.TemporaryDirectory(prefix='ribbity_') as _testdir:
        print(f'running tests in temp directory {_testdir}')

        shutil.copy(path_to('..', 'ribbity-test.dmp'), _testdir)
        shutil.copy(path_to('test-files', 'config-test-alt-site-2.toml'),
                    _testdir)
        shutil.copytree(path_to('test-files', 'site-templates.test'),
                        os.path.join(_testdir,
                                     'tests',
                                     'test-files',
                                     'site-templates.test'))

        cwd = os.getcwd()
        os.chdir(_testdir)

        print(f'running ribbity.main_build.main')
        retval = main_build('config-test-alt-site-2.toml')
        assert retval == 0

        # run the tests!
        try:
            yield
        finally:
            os.chdir(cwd)

    # teardown here, if anything.
    # note: temp directory should be removed automatically by context mgr.
    print('done with tests!')


def build_path(filename):
    return os.path.join(_testdir, 'docsdocs2', filename)


def load_md(filename):
    with open(build_path(filename), 'rt') as fp:
        md = fp.read()

    md = md.lstrip()

    return md

### tests!


def test_pull_issue1_excluded():
    issue = get_issue_by_number(1)

    # should NOT be ignored
    assert not issue.is_ignored

    # should NOT be included by this config
    assert not os.path.exists(build_path('1-test-issue-number-1.md'))


def test_pull_issue13_not_excluded():
    issue = get_issue_by_number(13)

    # should NOT be ignored
    assert not issue.is_ignored

    # SHOULD be included by this config
    assert os.path.exists(build_path('13-test-include-and-exclude-criteria-based-on-labels.md'))
