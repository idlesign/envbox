import pytest

from envbox.utils import cast_type


def test_cast_type():

    assert cast_type('1.a0') == '1.a0'
    assert cast_type('some') == 'some'
    assert cast_type('10') == 10
    assert cast_type('True') is True
