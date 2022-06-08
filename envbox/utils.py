import io
import os
import re
from ast import literal_eval
from pathlib import Path
from typing import Any, Union

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


def read_envfile(fpath: Union[str, Path]) -> dict:
    """Reads environment variables from .env key-value file.

    Rules:
        * Lines starting with # (hash) considered comments. Inline comments not supported;
        * Multiline values are supported (require to be quoted with \n inside values or actual unix newlines);
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

        with io.open(f'{fpath}') as f:
            lines = f.readlines()

    except IOError:
        return env_vars

    def drop_quotes(quote_char, val):
        if val.startswith(quote_char) and val.endswith(quote_char):
            val = val.replace('\\n', '\n').strip(quote_char)
        return val

    idx = 0

    while True:

        try:
            line = lines[idx].strip()

        except IndexError:
            # no more lines
            break

        if not line or line.startswith('#'):
            idx += 1
            continue

        key, _, val = line.partition('=')
        key = key.strip()

        if not key:
            idx += 1
            continue

        val = val.strip()

        ahead_bag = []

        if val == '"' or (val.startswith('"') and not val.endswith('"')):
            # check ahead whether there is a multiple lines value
            for ahead_idx in range(idx+1, len(lines)):
                ahead_line = lines[ahead_idx].strip()
                ahead_key, _, _ = ahead_line.partition('=')
                ahead_key = ahead_key.strip()

                if ahead_key and (ahead_line != ahead_key) and ahead_key.upper() == ahead_key:
                    # next definition is valid stop here
                    break

                ahead_bag.append(ahead_line)
                idx += 1

        if ahead_bag:
            # normalize into a string with \n
            if val != '"':
                # do not insert an empty line if there's a single dangling "
                val = f'{val}\\n'
            val = f'{val}' + '\\n'.join(ahead_bag)
            ahead_bag.clear()

        val = drop_quotes("'", drop_quotes('"', val))

        for match in RE_TPL_VAR.findall(val):
            var_tpl, var_name = match

            var_val = environ.get(var_name)

            if var_val is None:
                var_val = env_vars.get(var_name)

            if var_val is not None:
                val = val.replace(var_tpl, var_val, 1)

        env_vars[key] = val
        idx += 1

    return env_vars
