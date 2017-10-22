import os

import pytest

from envbox import get_environment, PRODUCTION, import_by_environment


def test_get_environment():

    env = get_environment()

    assert env.is_development
    assert not env.is_production

    env_var = 'MY_ENV'

    os.environ[env_var] = PRODUCTION

    env = get_environment(detectors_opts={
        'environ': {'source': env_var}
    })

    assert env.is_production
    assert env == PRODUCTION


def test_autoimport(monkeypatch):

    with pytest.raises((ImportError, SystemError)):
        import_by_environment()

    def import_it(*args):
        return type('DummyModule', (object,), {})

    monkeypatch.setattr('envbox.base.import_module', import_it)
    env = import_by_environment()

    assert env.is_development
