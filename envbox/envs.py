from __future__ import unicode_literals, absolute_import

from collections import OrderedDict

from .utils import string_types, PY3


DEVELOPMENT = 'development'
TESTING = 'testing'
STAGING = 'staging'
PRODUCTION = 'production'

TYPES = OrderedDict()


class EnvironmentType(object):

    name = 'dummy'

    is_development = False
    is_testing = False
    is_staging = False
    is_production = False

    def __str__(self):
        name = self.name

        if not PY3:
            name = name.encode('utf-8')

        return name

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

    """
    if isinstance(env_type, string_types):
        env_type = TYPES[env_type]

    if alias is None:
        alias = env_type.name

    TYPES[alias] = env_type


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
