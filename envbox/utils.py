import io
import os
import re
from ast import literal_eval
from typing import Any

RE_TPL_VAR = re.compile('(\${([^}]+)})')


def cast_type(value: str) -> Any:
    """Try to cast value into Python native type.

    Returns non casted on errors.

    :param value:

    """
    result = value

    try:
        result = literal_eval(value)

    except Exception:
        pass

    return result


def read_envfile(fpath: str) -> dict:
    """Reads environment variables from .env key-value file.

    Rules:
        * Lines starting with # (hash) considered comments. Inline comments not supported;
        * Multiline values not supported.
        * Invalid lines are ignored;
        * Matching opening-closing quotes are stripped;
        * ${VAL} will be replaced with VAL value previously defined in .env file(s)
          or currently available in env.

    Returns a dictionary. Empty dictionary is returned if file is not accessible.

    :param fpath:

    """
    environ = os.environ
    env_vars = {}

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
