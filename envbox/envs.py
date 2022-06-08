import os
from typing import Union, Type, List, Sequence, Any, Dict

from .utils import cast_type, read_envfile

DEVELOPMENT = 'development'
TESTING = 'testing'
STAGING = 'staging'
PRODUCTION = 'production'

TYPES: Dict[str, Type['Environment']] = {}


class Environment:

    name: str = 'dummy'
    """Name this environment type is known as."""

    aliases: List[str] = []
    """Aliases this environment type is known as."""

    type_cast: bool = False
    """Whether to cast values into Python natives in .get() and .getmany() by default."""

    is_development: bool = False
    """Indicates whether this environment is development."""

    is_testing: bool = False
    """Indicates whether this environment is testing."""

    is_staging: bool = False
    """Indicates whether this environment is staging."""

    is_production: bool = False
    """Indicates whether this environment is production."""

    env = os.environ

    def __init__(self, name: str = None, type_cast: bool = None):
        """
        :param name: Environment name.

            .. note:: This will prevail over class attribute.

        :param type_cast: Whether to cast values into Python natives in .get() and .getmany() by default.

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
        env_vars = {}

        for fname in files:
            env_vars.update(read_envfile(fname))

        self.setmany(env_vars, overwrite=False)

    def getmany(self, prefix: str = '', type_cast: bool = None) -> dict:
        """Returns a dictionary of values for keys the given prefix.

        :param prefix:

        :param type_cast: Try to cast value into Python native type.

        """
        if type_cast is None:
            type_cast = self.type_cast

        result = {}

        for key, val in self.env.items():
            if key.startswith(prefix):

                if type_cast:
                    val = cast_type(val)

                result[key.replace(prefix, '', 1)] = val

        return result

    def getmany_casted(self, prefix: str = '') -> dict:
        """The same as `getnamy` but tries to cast values into Python natives."""
        return self.getmany(prefix=prefix, type_cast=True)

    def setmany(self, key_val: dict, prefix: str = '', overwrite: bool = True):
        """Sets values in batch mode.

        :param key_val:

        :param prefix:

        :param overwrite: Whether to overwrite value if it's already set.

        """
        key_val = key_val or {}
        env = self.env

        for key, val in key_val.items():
            key = f'{prefix}{key}'
            val = f'{val}'

            if overwrite:
                env[key] = val

            else:
                env.setdefault(key, val)

    def dropmany(self, keys: Sequence[str] = None, prefix: str = ''):
        """Drops keys in batch mode.

        :param keys: Keys to drop. If not set current env keys will be used.

        :param prefix:

        """
        env = self.env

        keys = keys or [key.replace(prefix, '', 1) for key in env.keys() if key.startswith(prefix)]

        for key in keys:
            del env[f'{prefix}{key}']

    def get(self, key: str, default: Any = None, type_cast: bool = None) -> Any:
        """Get environment variable value.

        :param key:

        :param default: Default value to return if no value found.

        :param type_cast: Try to cast value into Python native type.

        """
        result = self.env.get(key, default)

        if type_cast is None:
            type_cast = self.type_cast

        if result is not default and type_cast:
            result = cast_type(result)

        return result

    def get_casted(self, key: str, default: Any = None) -> Any:
        """The same as `get` but tries to cast values into Python natives."""
        return self.get(key, default, type_cast=True)

    def set(self, key: str, value: Any, overwrite: bool = True):
        """Set environment variable.

        :param key:

        :param value:

        :param overwrite: Whether to overwrite value if it's already set.

        """
        value = f'{value}'

        if overwrite:
            self.env[key] = value

        else:
            self.env.setdefault(key, value)

    def drop(self, key: str):
        """Removes key from environment."""
        del self.env[key]
        
    def keys(self):
        # mapping protocol: allow casting to a dict
        return list(self.env.keys())

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
        return f'{self}' == f'{other}'


class Development(Environment):
    """Development (local) environment."""

    name: str = DEVELOPMENT
    aliases: List[str] = ['dev']
    is_development: bool = True


class Testing(Environment):
    """Testing environment."""

    name: str = TESTING
    aliases: List[str] = ['test']
    is_testing: bool = True


class Staging(Environment):
    """Staging (prestable) environment."""

    name: str = STAGING
    aliases: List[str] = ['stage']
    is_staging: bool = True


class Production(Environment):
    """Production (stable) environment."""

    name: str = PRODUCTION
    aliases: List[str] = ['prod']
    is_production: bool = True


TypeEnvArg = Union[Type['Environment'], str]


def register_type(env_type: TypeEnvArg, alias: str = None) -> Type[Environment]:
    """Registers environment type.

    :param env_type: Environment type or its alias
        (for already registered types).

    :param alias: Alias to register type under. If not set type name is used.

    """
    if isinstance(env_type, str):
        env_type = TYPES[env_type]

    if alias is None:
        alias = env_type.name

    TYPES[alias] = env_type

    for alias in env_type.aliases:
        TYPES[alias] = env_type

    return env_type


def get_type(cls_or_alias: TypeEnvArg) -> Type[Environment]:
    """Returns environment type by alias (or class itself)

    :param cls_or_alias:

    """
    if isinstance(cls_or_alias, str):
        return TYPES[cls_or_alias]

    return cls_or_alias


def __register_builtins():

    if TYPES:  # pragma: nocover
        return

    for cls in [Development, Testing, Staging, Production]:
        register_type(cls)


__register_builtins()
