import pytest

from envbox import get_environment
from envbox.detectors import get_detector, Environ, File


def test_get_detector():

    assert get_detector(Environ) is Environ
    assert get_detector('environ') is Environ

    with pytest.raises(KeyError):
        get_detector('bogus')


def test_file_detector():
    detector = get_detector('file')

    assert detector is File

    env = get_environment(detectors_opts={'file': {'source': 'myenvironment'}})

    assert env.is_testing
