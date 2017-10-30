from os.path import dirname, basename
from inspect import currentframe
from importlib import import_module

from .detectors import DETECTORS, get_detector
from .envs import Environment, DEVELOPMENT, get_type


def get_environment(default=DEVELOPMENT, detectors=None, detectors_opts=None, use_envfiles=True):
    """Returns current environment type object.

    :param str|Environment|None default: Default environment type or alias.

    :param list[Detector] detectors: List of environment detectors to be used in chain.
        If not set, default builtin chain is used.

    :param dict detectors_opts: Detectors options dictionary.
        Where keys are detector names and values are keyword arguments dicts.

    :param bool use_envfiles: Whether to set environment variables (if not already set)
        using data from .env files.

    :rtype: Environment|None
    """
    detectors_opts = detectors_opts or {}

    if detectors is None:
        detectors = DETECTORS.keys()

    env = None

    for detector in detectors:
        opts = detectors_opts.get(detector, {})
        detector = get_detector(detector)

        detector = detector(**opts)
        env_name = detector.probe()

        if env_name:
            env = get_type(env_name)
            break

    if env is None and default is not None:
        env = get_type(default)

    if env is not None:
        env = env()  # type: Environment
        use_envfiles and env.update_from_envfiles()

    return env


def import_by_environment(environment=None, module_name_pattern='settings_%s', silent=False):
    """Automatically imports symbols of a submodule of a package for given
    (or detected) environment into globals of an entry-point submodule.

    Example::

        - project
        --- __init__.py
        --- settings.py
        --- settings_development.py

    * Here ``project`` is a package available for import (note ``__init__.py``).

    * ``settings.py`` is an entry point module for settings using ``import_by_environment()``.

    * ``settings_development.py`` is one of module files for certain environment (development).

    * ``import_by_environment()`` call in ``settings.py`` makes symbols from ``settings_development.py``
      available from ``settings.py``.

    :param Environment environment:

    :param str|unicode module_name_pattern: Environment submodule name pattern.
        ``%s`` will be replaced with environment name.

    :param bool silent: If ``True`` no import error (if any) will be raised.

    :rtype: Environment|None

    :returns: ``Environment`` object if module is imported or ``None``.

    """
    environment = environment or get_environment()

    module_name_pattern = '.' + module_name_pattern

    settings_module = currentframe().f_back
    package_name = basename(dirname(settings_module.f_code.co_filename))

    result = None

    try:
        env_module = import_module(module_name_pattern % environment, package_name)
        settings_module.f_globals.update(env_module.__dict__)

        result = environment

    except (ImportError, SystemError):
        if not silent:
            raise

    return result
