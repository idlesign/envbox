from os import path

from envbox import Environment
from envbox.utils import cast_type, read_envfile


def test_cast_type():

    assert cast_type('1.a0') == '1.a0'
    assert cast_type('some') == 'some'
    assert cast_type('10') == 10
    assert cast_type('True') is True


def test_read_envfile():

    env = Environment()
    env['ENVBOXTST_CHANGE'] = 'this'

    entries = read_envfile(path.join(path.dirname(__file__), 'testapp', '.env'))

    assert len(entries) == 5
    assert entries['ENVBOXTST_MYQUOTED1'] == 'some quoted'
    assert entries['ENVBOXTST_MYQUOTED2'] == 'some "2" quoted'
    assert entries['ENVBOXTST_MYVAL2'] == 'enim'
    assert entries['ENVBOXTST_MYVAL1'] == 'mine'
    assert entries['ENVBOXTST_OTHER'] == 'mine this $VAL enim'

    del env['ENVBOXTST_CHANGE']
