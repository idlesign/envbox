import os

import pytest

from envbox.detectors import get_detector, Environ


def test_get_detector():

    assert get_detector(Environ) is Environ
    assert get_detector('environ') is Environ

    with pytest.raises(KeyError):
        get_detector('bogus')

