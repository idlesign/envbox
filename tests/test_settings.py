import pytest

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


def test_typed_settings(monkeypatch):

    class _Typed(SettingsBase):

        COUNT: int = 3
        RATIO: float = 1.5
        DEBUG: bool = False
        TITLE: str = "mine"
        ALIASED: "int" = 7
        ITEMS: list[str] = []
        LEGACY = "untouched"

    Settings = _Typed()

    assert Settings.COUNT == 3
    assert Settings.DEBUG is False
    assert Settings.ITEMS == []

    monkeypatch.setenv("COUNT", "10")
    monkeypatch.setenv("RATIO", "2.5")
    monkeypatch.setenv("DEBUG", "yes")
    monkeypatch.setenv("TITLE", "theirs")
    monkeypatch.setenv("ALIASED", "42")
    monkeypatch.setenv("LEGACY", "untouched too")

    assert Settings.COUNT == 10
    assert Settings.RATIO == 2.5
    assert Settings.DEBUG is True
    assert Settings.TITLE == "theirs"
    assert Settings.ALIASED == 42
    assert Settings.LEGACY == "untouched too"


@pytest.mark.parametrize("value", ["1", "TRUE", "yes", "On"])
def test_typed_settings_bool_true(monkeypatch, value):

    class _TypedBool(SettingsBase):

        FLAG: bool = False

    monkeypatch.setenv("FLAG", value)

    assert _TypedBool().FLAG is True


@pytest.mark.parametrize("value", ["", "0", "FALSE", "no", "Off"])
def test_typed_settings_bool_false(monkeypatch, value):

    class _TypedBool(SettingsBase):

        FLAG: bool = True

    monkeypatch.setenv("FLAG", value)

    assert _TypedBool().FLAG is False


def test_typed_settings_invalid(monkeypatch):

    class _TypedInvalid(SettingsBase):

        COUNT: int = 3
        DEBUG: bool = False

    Settings = _TypedInvalid()

    monkeypatch.setenv("COUNT", "not a number")

    with pytest.raises(ValueError, match="Unable to cast COUNT"):
        Settings.COUNT

    monkeypatch.setenv("DEBUG", "maybe")

    with pytest.raises(ValueError, match="Unable to cast DEBUG"):
        Settings.DEBUG
