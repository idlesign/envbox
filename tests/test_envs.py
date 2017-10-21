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


def test_set_get():

    env = Development()
    env.set('one', 1)

    assert env.get('one') == '1'

    env['one'] = 2
    assert env.get('one') == '2'

    env.one = 3
    assert env.one == '3'


def test_set_get_many():

    env = Development()
    env.setmany('ENVBOX_', {'one': 1, 'TWO': 2})

    many = env.getmany('ENVBOX_')

    assert many['one'] == '1'
    assert many['TWO'] == '2'
