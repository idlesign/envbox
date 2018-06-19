import io
import os
import re
import sys
from ast import literal_eval
from collections import OrderedDict

RE_TPL_VAR = re.compile('(\${([^}]+)})')

PY3 = sys.version_info[0] == 3

if PY3:  # pragma: nocover
    string_types = str,

else:  # pragma: nocover
    string_types = basestring,


def python_2_unicode_compatible(klass):  # pragma: nocover
    if not PY3:
        klass.__unicode__ = klass.__str__
        klass.__str__ = lambda self: self.__unicode__().encode('utf-8')
    return klass


def add_metaclass(metaclass):
    """Class decorator for creating a class with a metaclass."""
    def wrapper(cls):
        orig_vars = cls.__dict__.copy()
        orig_vars.pop('__dict__', None)
        orig_vars.pop('__weakref__', None)
        return metaclass(cls.__name__, cls.__bases__, orig_vars)
    return wrapper


def cast_type(value):
    """Try to cast value into Python native type.

    Returns non casted on errors.

    :param str|unicode value:

    :rtype: Any
    """
    result = value

    try:
        result = literal_eval(value)

    except Exception:
        pass

    return result


def read_envfile(fpath):
    """Reads environment variables from .env key-value file.

    Rules:
        * Lines starting with # (hash) considered comments. Inline comments not supported;
        * Multiline values not supported.
        * Invalid lines are ignored;
        * Matching opening-closing quotes are stripped;
        * ${VAL} will be replaced with VAL value previously defined in .env file(s)
          or currently available in env.

    Returns a dictionary.

    Empty dictionary is returned if file is not accessible.

    :param str|unicode fpath:

    :rtype: OrderedDict

    """
    environ = os.environ
    env_vars = OrderedDict()

    try:

        with io.open(fpath) as f:
            lines = f.readlines()

    except IOError:
        return env_vars

    def drop_quotes(quote_char, val):
        if val.startswith(quote_char) and val.endswith(quote_char):
            val = val.strip(quote_char).strip()
        return val

    for line in lines:
        line = line.strip()

        if not line or line.startswith('#'):
            continue

        key, _, val = line.partition('=')

        key = key.strip()
        val = drop_quotes("'", drop_quotes('"', val.strip()))

        if not key:
            continue

        for match in RE_TPL_VAR.findall(val):
            var_tpl, var_name = match

            var_val = environ.get(var_name)

            if var_val is None:
                var_val = env_vars.get(var_name)

            if var_val is not None:
                val = val.replace(var_tpl, var_val, 1)

        env_vars[key] = val

    return env_vars
