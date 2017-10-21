import os

import pytest

from envbox import DEVELOPMENT
from envbox.envs import get_type, register_type, Development


def test_get_type():

    assert get_type(Development) is Development
    assert get_type('development') is Development

    with pytest.raises(KeyError):
        get_type('bogus')


def test_register_type():

    dev_alias = 'dev'

    new_type = register_type(DEVELOPMENT, dev_alias)

    assert new_type is Development
