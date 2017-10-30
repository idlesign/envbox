from __future__ import unicode_literals, absolute_import

import os
from collections import OrderedDict

from .utils import string_types, python_2_unicode_compatible, cast_type, read_envfile

DEVELOPMENT = 'development'
TESTING = 'testing'
STAGING = 'staging'
PRODUCTION = 'production'

TYPES = OrderedDict()


@python_2_unicode_compatible
class Environment(object):

    name = 'dummy'
    """Name this environment type is known as."""

    aliases = []
    """Aliases this environment type is known as."""

    type_cast = False
    """Whether to cast values into Python natives in .get() and .getmany() by default."""

    is_development = False
    """Indicates whether this environment is development."""

    is_testing = False
    """Indicates whether this environment is testing."""

    is_staging = False
    """Indicates whether this environment is staging."""

    is_production = False
    """Indicates whether this environment is production."""

    env = os.environ

    def __init__(self, name=None, type_cast=None):
        """
        :param str|unicode name: Environment name.

            .. note:: This will prevail over class attribute.

        :param bool type_cast: Whether to cast values into Python natives in .get() and .getmany() by default.

            .. note:: This will prevail over class attribute.

        """
        self.name = name or self.name
        self.type_cast = type_cast or self.type_cast

    def update_from_envfiles(self):
        """Updates environment variables (if not already set) using data from .env files.

        Files used (as they read; values read later override previous values):
            * .env
            * .env.<env_name>
            * .env.local
            * .env.<env_name>.local

            <env_name> - Environment name (e.g. ``production``, ``development`` etc.)

        """
        name_candidates = [self.name]
        name_candidates.extend(self.aliases)

        def contribute_candidates(tpl):
            # This will handle env type aliases.
            for candidate in name_candidates:
                files.append(tpl % candidate)

        files = ['.env']
        contribute_candidates('.env.%s')
        files.append('.env.local')
        contribute_candidates('.env.%s.local')
        env_vars = OrderedDict()

        for fname in files:
            env_vars.update(read_envfile(fname))

        self.setmany(env_vars, overwrite=False)

    def getmany(self, prefix='', type_cast=None):
        """Returns a dictionary of values for keys the given prefix.

        :param str|unicode prefix:

        :param bool type_cast: Try to cast value into Python native type.

        :rtype: OrderedDict

        """
        if type_cast is None:
            type_cast = self.type_cast

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

    def setmany(self, key_val, prefix='', overwrite=True):
        """Sets values in batch mode.

        :param dict key_val:

        :param str|unicode prefix:

        :param bool overwrite: Whether to overwrite value if it's already set.

        """
        key_val = key_val or {}
        env = self.env

        for key, val in key_val.items():
            key = prefix + key
            val = '%s' % val

            if overwrite:
                env[key] = val

            else:
                env.setdefault(key, val)

    def dropmany(self, keys=None, prefix=''):
        """Drops keys in batch mode.

        :param Iterable keys: Keys to drop. If not set current env keys will be used.

        :param str|unicode prefix:

        """
        env = self.env

        keys = keys or [key.replace(prefix, '', 1) for key in env.keys() if key.startswith(prefix)]

        for key in keys:
            del env[prefix + key]

    def get(self, key, default=None, type_cast=None):
        """Get environment variable value.

        :param str|unicode key:

        :param default: Default value to return if no value found.

        :param bool type_cast: Try to cast value into Python native type.

        """
        result = self.env.get(key, default)

        if type_cast is None:
            type_cast = self.type_cast

        if result is not default and type_cast:
            result = cast_type(result)

        return result

    def get_casted(self, key, default=None):
        """The same as `get` but tries to cast values into Python natives."""
        return self.get(key, default, type_cast=True)

    def set(self, key, value, overwrite=True):
        """Set environment variable.

        :param str|unicode key:

        :param value:

        :param bool overwrite: Whether to overwrite value if it's already set.

        """
        value = '%s' % value

        if overwrite:
            self.env[key] = value

        else:
            self.env.setdefault(key, value)

    def drop(self, key):
        """Removes key from environment."""
        del self.env[key]

    __delattr__ = __delitem__ = drop
    __getattr__ = __getitem__ = get
    __setitem__ = set

    def __setattr__(self, key, value):

        try:
            self.__getattribute__(key)

            object.__setattr__(self, key, value)

        except AttributeError:
            self.set(key, value)

    def __contains__(self, key):
        return key in self.env

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return '%s' % self == '%s' % other


class Development(Environment):
    """Development (local) environment."""

    name = DEVELOPMENT
    aliases = ['dev']
    is_development = True


class Testing(Environment):
    """Testing environment."""

    name = TESTING
    aliases = ['test']
    is_testing = True


class Staging(Environment):
    """Staging (prestable) environment."""

    name = STAGING
    aliases = ['stage']
    is_staging = True


class Production(Environment):
    """Production (stable) environment."""

    name = PRODUCTION
    aliases = ['prod']
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

    for alias in env_type.aliases:
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
