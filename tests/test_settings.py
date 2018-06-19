from envbox import get_environment
from envbox.settings import SettingsBase


def test_settings():

    class _Settings(SettingsBase):

        ONE = 1
        SOME = 'two'
        ANOTHER = True

    Settings = _Settings()

    assert Settings.ONE == 1
    assert Settings.SOME == 'two'
    assert Settings.ANOTHER

    if Settings.ANOTHER:
        Settings.SOME = 'three'

    assert Settings.SOME == 'three'

    env = get_environment()
    env['ONE'] = 2

    assert Settings.ONE == 2

    # assert no env found
    Settings.get_environment = lambda *args, **kwargs: None

    assert Settings.ANOTHER
