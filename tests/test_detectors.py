import pytest

from envbox import get_environment
from envbox.detectors import get_detector, Environ, File


def test_get_detector():

    assert get_detector(Environ) is Environ
    assert get_detector('environ') is Environ

    with pytest.raises(KeyError):
        get_detector('bogus')


def test_file_detector(tmpdir):
    detector = get_detector('file')

    assert detector is File

    path = tmpdir.mkdir('envboxtmp').join('myenvironment')
    path.write('testing')

    env = get_environment(detectors_opts={'file': {'source': '%s' % path}})

    assert env.is_testing
