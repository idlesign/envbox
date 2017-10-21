import os

import pytest

from envbox import get_environment, PRODUCTION


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
