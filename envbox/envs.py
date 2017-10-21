from __future__ import unicode_literals, absolute_import
import os

from collections import OrderedDict

from .utils import string_types, python_2_unicode_compatible


DEVELOPMENT = 'development'
TESTING = 'testing'
STAGING = 'staging'
PRODUCTION = 'production'

TYPES = OrderedDict()


@python_2_unicode_compatible
class EnvironmentType(object):

    name = 'dummy'

    is_development = False
    is_testing = False
    is_staging = False
    is_production = False

    def getmany(self, prefix):
        """Returns a dictionary of values for keys the given prefix.

        :param str|unicode prefix:

        :rtype: OrderedDict

        """
        result = OrderedDict()

        for key, val in os.environ.items():
            if key.startswith(prefix):
                result[key.replace(prefix, '', 1)] = val

        return result

    def setmany(self, prefix, key_val):
        """Sets values

        :param str|unicode prefix:

        :param dict key_val:

        """
        key_val = key_val or {}
        env = os.environ

        for key, val in key_val.items():
            env[prefix + key] = '%s' % val

    def get(self, key, default=None):
        """Get environment variable value.

        :param str|unicode key:

        :param default: Default value to return if no value found.

        """
        result = os.environ.get(key, default)

        return result

    def set(self, key, value):
        """Set environment variable.

        :param str|unicode key:

        :param value:

        """
        os.environ[key] = '%s' % value

    __getattr__ = __getitem__ = get
    __setattr__ = __setitem__ = set

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return '%s' % self == '%s' % other


class Development(EnvironmentType):
    """Development (local) environment."""

    name = DEVELOPMENT
    is_development = True


class Testing(EnvironmentType):
    """Testing environment."""

    name = TESTING
    is_testing = True


class Staging(EnvironmentType):
    """Staging (prestable) environment."""

    name = STAGING
    is_staging = True


class Production(EnvironmentType):
    """Production (stable) environment."""

    name = PRODUCTION
    is_production = True


def register_type(env_type, alias=None):
    """Registers environment type.

    :param str|unicode|EnvironmentType env_type: Environment type or its alias
        (for already registered types).

    :param str|unicode alias: Alias to register type under. If not set type name is used.

    :rtype: EnvironmentType

    """
    if isinstance(env_type, string_types):
        env_type = TYPES[env_type]

    if alias is None:
        alias = env_type.name

    TYPES[alias] = env_type

    return env_type


def get_type(cls_or_alias):
    """Returns environment type by alias (or class itself)

    :param EnvironmentType|str|unicode cls_or_alias:

    :rtype: EnvironmentType

    """
    if isinstance(cls_or_alias, string_types):
        return TYPES[cls_or_alias]

    return cls_or_alias


def __register_builtins():

    if TYPES:  # pragma: nocover
        return

    for cls in [Development, Testing, Staging, Production]:
        register_type(cls)


__register_builtins()
