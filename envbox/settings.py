from threading import local
from typing import Optional, Any

from .base import get_environment

if False:  # pragma: nocover
    from .envs import Environment  # noqa


_LOCALS = local()
_UNSET = tuple()

setattr(_LOCALS, 'envbox_settings', {})


class _SettingsMeta(type):

    def __new__(cls, name, bases, namespace, **kwargs):

        for attr_name, attr_val in namespace.items():
            if attr_name == attr_name.upper():
                namespace[attr_name] = _Setting(attr_name, attr_val)

        return type.__new__(cls, name, bases, dict(namespace))


class _Setting:

    def __init__(self, name: str, default: Any):
        self.name = name
        self.default = default

    def __get__(self, instance: 'SettingsBase', owner):

        try:
            return _LOCALS.envbox_settings[self.name]

        except KeyError:
            env = instance.get_environment()
            if not env:
                return self.default
            return env.get_casted(self.name, default=self.default)

    def __set__(self, instance, value):
        _LOCALS.envbox_settings[self.name] = value


class SettingsBase(metaclass=_SettingsMeta):
    """Use this class as base for your classes containing settings.

    .. note:: Settings are per-thread.

    Every uppercase attribute of of a heir class will be treated
    as a setting.

    Accessing any setting which was not set in the session,
    will lead to appropriate environment variable probing, thus:

        1. current session value
        2. environment value
        3. default value

    .. code-block:: python

        class _Settings(SettingsBase):

            ONE = 1
            SOME = 'two'
            ANOTHER = True

        Settings = _Settings()

        if Settings.ANOTHER:
            Settings.SOME = 'three'

    """

    def get_environment(self) -> Optional['Environment']:
        """Return current environment.

        This could be customized by a child if required.

        """
        return get_environment()
