"Test config file stuff."
import pytest
import os


from ribbity.config import RibbityConfig


thisdir = os.path.dirname(os.path.abspath(__file__))
def path_to(*p):
    return os.path.join(thisdir, *p)

def test_load_1():
    # test basic attribute retrieval stuff
    config = RibbityConfig.load(path_to('test-files', 'config-test-1.toml'))

    assert config.title == 'ribbity-tests'
    assert config.get('title') == 'ribbity-tests'

    with pytest.raises(AttributeError):
        _ = config.NOEXIST

    assert config.get('NOEXIST', 'a value') == 'a value'
