from __future__ import unicode_literals, absolute_import

import os
from functools import partial
from collections import OrderedDict

from .utils import string_types, python_2_unicode_compatible, cast_type

DEVELOPMENT = 'development'
TESTING = 'testing'
STAGING = 'staging'
PRODUCTION = 'production'

TYPES = OrderedDict()


@python_2_unicode_compatible
class Environment(object):

    name = 'dummy'

    is_development = False
    """Indicates whether this environment is development."""

    is_testing = False
    """Indicates whether this environment is testing."""

    is_staging = False
    """Indicates whether this environment is staging."""

    is_production = False
    """Indicates whether this environment is production."""

    env = os.environ

    def getmany(self, prefix='', type_cast=False):
        """Returns a dictionary of values for keys the given prefix.

        :param str|unicode prefix:

        :param bool type_cast: Try to cast value into Python native type.

        :rtype: OrderedDict

        """
        result = OrderedDict()

        for key, val in self.env.items():
            if key.startswith(prefix):

                if type_cast:
                    val = cast_type(val)

                result[key.replace(prefix, '', 1)] = val

        return result

    def getmany_casted(self, prefix=''):
        """The same as `getnamy` but tries to cast values into Python natives."""
        return self.getmany(prefix=prefix, type_cast=True)

    def setmany(self, key_val, prefix=''):
        """Sets values in batch mode.

        :param dict key_val:

        :param str|unicode prefix:

        """
        key_val = key_val or {}
        env = self.env

        for key, val in key_val.items():
            env[prefix + key] = '%s' % val

    def dropmany(self, keys, prefix=''):
        """Drops keys in batch mode.

        :param Iterable keys:

        :param str|unicode prefix:

        """
        env = self.env

        for key in keys:
            del env[prefix + key]

    def get(self, key, default=None, type_cast=False):
        """Get environment variable value.

        :param str|unicode key:

        :param default: Default value to return if no value found.

        :param bool type_cast: Try to cast value into Python native type.

        """
        result = self.env.get(key, default)

        if result is not default and type_cast:
            result = cast_type(result)

        return result

    def get_casted(self, key, default=None):
        """The same as `get` but tries to cast values into Python natives."""
        return self.get(key, default, type_cast=True)

    def set(self, key, value):
        """Set environment variable.

        :param str|unicode key:

        :param value:

        """
        self.env[key] = '%s' % value

    def drop(self, key):
        """Removes key from environment."""
        del self.env[key]

    __delattr__ = __delitem__ = drop
    __getattr__ = __getitem__ = get
    __setattr__ = __setitem__ = set

    def __contains__(self, key):
        return key in self.env

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return '%s' % self == '%s' % other


class Development(Environment):
    """Development (local) environment."""

    name = DEVELOPMENT
    is_development = True


class Testing(Environment):
    """Testing environment."""

    name = TESTING
    is_testing = True


class Staging(Environment):
    """Staging (prestable) environment."""

    name = STAGING
    is_staging = True


class Production(Environment):
    """Production (stable) environment."""

    name = PRODUCTION
    is_production = True


def register_type(env_type, alias=None):
    """Registers environment type.

    :param str|unicode|Environment env_type: Environment type or its alias
        (for already registered types).

    :param str|unicode alias: Alias to register type under. If not set type name is used.

    :rtype: Environment

    """
    if isinstance(env_type, string_types):
        env_type = TYPES[env_type]

    if alias is None:
        alias = env_type.name

    TYPES[alias] = env_type

    return env_type


def get_type(cls_or_alias):
    """Returns environment type by alias (or class itself)

    :param Environment|str|unicode cls_or_alias:

    :rtype: Environment

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
