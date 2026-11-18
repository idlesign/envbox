from inspect import get_annotations
from threading import local
from typing import TYPE_CHECKING, Any, Optional

from .base import get_environment

if TYPE_CHECKING:
    from .envs import Environment


_LOCALS = local()
_UNSET = ()

_LOCALS.envbox_settings = {}

_HINT_ALIASES: dict[str, type] = {
    "bool": bool,
    "float": float,
    "int": int,
    "str": str,
}
"""Type aliases used when annotations are strings (e.g. with postponed evaluation)."""

_TRUE_VALUES = {"1", "true", "yes", "on"}
_FALSE_VALUES = {"", "0", "false", "no", "off"}


def _resolve_hint(hint: Any) -> type | None:
    """Resolves a type hint (possibly a string) into a type suitable
    for value casting. Returns None if the hint is not usable.

    :param hint:

    """
    if isinstance(hint, str):
        return _HINT_ALIASES.get(hint)

    if isinstance(hint, type):
        return hint

    return None


def _cast_setting_value(value: str, *, hint: type, name: str) -> Any:
    """Casts an environment variable value into the given type.

    Raises ValueError if casting is not possible.

    :param value:

    :param hint:

    :param name: Setting name (used in error messages).

    """
    if hint is bool:
        val = value.strip().lower()

        if val in _TRUE_VALUES:
            return True

        if val in _FALSE_VALUES:
            return False

    else:

        try:
            return hint(value)

        except (TypeError, ValueError):
            pass

    raise ValueError(f"Unable to cast {name} setting value into {hint.__name__}")


class _SettingsMeta(type):

    def __new__(cls, name, bases, namespace, **kwargs):
        new_cls = type.__new__(cls, name, bases, dict(namespace))

        # get_annotations is used instead of direct __annotations__ access
        # for compatibility with lazy annotations evaluation (Python 3.14+).
        annotations = get_annotations(new_cls)

        for attr_name, attr_val in namespace.items():
            if attr_name == attr_name.upper():
                hint = _resolve_hint(annotations.get(attr_name))
                setattr(new_cls, attr_name, _Setting(attr_name, default=attr_val, hint=hint))

        return new_cls


class _Setting:

    def __init__(self, name: str, *, default: Any, hint: type | None = None):
        self.name = name
        self.default = default
        self.hint = hint

    def __get__(self, instance: 'SettingsBase', owner):

        try:
            return _LOCALS.envbox_settings[self.name]

        except KeyError:
            env = instance.get_environment()
            if not env:
                return self.default

            if self.hint is None:
                return env.get_casted(self.name, default=self.default)

            value = env.get(self.name)

            if value is None:
                return self.default

            return _cast_setting_value(value, hint=self.hint, name=self.name)

    def __set__(self, instance, value):
        _LOCALS.envbox_settings[self.name] = value


class SettingsBase(metaclass=_SettingsMeta):
    """Use this class as base for your classes containing settings.

    !!! note
        Settings are per-thread.

    Every uppercase attribute of an heir class will be treated
    as a setting.

    Accessing any setting which was not set in the session,
    will lead to appropriate environment variable probing, thus:

        1. current session value
        2. environment value
        3. default value

    ```python
    class _Settings(SettingsBase):

        ONE = 1
        SOME = 'two'
        ANOTHER = True

    Settings = _Settings()

    if Settings.ANOTHER:
        Settings.SOME = 'three'
    ```

    A type annotation hint (if any) will be used to cast a value
    read from environment into the given type:

    ```python
    class _Settings(SettingsBase):

        THREADS: int = 1
        DEBUG: bool = False
    ```

    """

    def get_environment(self) -> Optional['Environment']:
        """Return current environment.

        This could be customized by a child if required.

        """
        return get_environment()
