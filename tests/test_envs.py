import os
import pytest

from envbox import get_environment
from envbox import DEVELOPMENT, PRODUCTION
from envbox.detectors import Environ
from envbox.envs import get_type, register_type, Development


def test_get_type():

    assert get_type(Development) is Development
    assert get_type('development') is Development

    with pytest.raises(KeyError):
        get_type('bogus')


def test_register_type(monkeypatch):

    dev_alias = 'dev'

    new_type = register_type(DEVELOPMENT, dev_alias)

    assert new_type is Development

    assert not get_environment().is_production

    prod_alias = 'prod'
    register_type(PRODUCTION, prod_alias)

    monkeypatch.setenv(Environ.source, prod_alias)

    assert get_environment().is_production


def test_set_get():

    env = Development()
    env.set('one', 1)

    assert env.get('one') == '1'

    env.set('one', 10, overwrite=False)
    assert env.get('one') == '1'

    env['one'] = 2
    assert env.get('one') == '2'
    assert env.get_casted('one') == 2

    env.one = 3
    assert env.one == '3'

    env.type_cast = True
    assert env.get('one') == 3


def test_set_get_many(datafix_dir):

    env = Development()

    env.setmany({'one': 1, 'TWO': 2}, prefix='ENVBOX_')
    many = env.getmany('ENVBOX_')

    assert many['one'] == '1'
    assert many['TWO'] == '2'

    env.setmany({'one': 1, 'TWO': 2}, prefix='ENVBOX_', overwrite=False)
    many = env.getmany('ENVBOX_')

    assert many['one'] == '1'
    assert many['TWO'] == '2'

    many = env.getmany_casted('ENVBOX_')

    assert many['one'] == 1
    assert many['TWO'] == 2

    cwd = os.getcwd()
    try:
        os.chdir(f'{datafix_dir}')
        env.update_from_envfiles()

        envbox_tst = env.getmany('ENVBOXTST_')

        assert envbox_tst['FROMLOCAL'] == 'yes'
        assert envbox_tst['FROMDEV'] == 'true'
        assert envbox_tst['FROMDEVLOCAL'] == '1'

        assert envbox_tst['MYQUOTED1'] == 'from_local'
        assert envbox_tst['MYQUOTED2'] == 'some "2" quoted'
        assert envbox_tst['MYVAL1'] == 'from_dev_local'
        assert envbox_tst['MYVAL2'] == 'enim'
        assert envbox_tst['OTHER'] == 'mine ${ENVBOXTST_CHANGE} $VAL enim'

        assert len(envbox_tst) == 13

    finally:
        env.dropmany(prefix='ENVBOXTST_')
        os.chdir(cwd)


def test_drop():
    env = Development()
    env.setmany({'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5})

    assert 'a' in env

    env.drop('a')

    assert 'a' not in env

    del env['b']

    assert 'b' not in env

    del env.c

    assert 'c' not in env

    env.dropmany(['d', 'e'])
    assert 'd' not in env
    assert 'e' not in env
