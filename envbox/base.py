import sys
from os.path import dirname, basename
from inspect import currentframe
from importlib import import_module
from typing import Union, Optional, List

from .detectors import DETECTORS, get_detector, Detector
from .envs import Environment, DEVELOPMENT, get_type


def get_environment(
        default: Optional[Union[str, Environment]] = DEVELOPMENT,
        detectors: List[Detector] = None,
        detectors_opts: dict = None,
        use_envfiles: bool = True
) -> Optional[Environment]:
    """Returns current environment type object.

    :param default: Default environment type or alias.

    :param detectors: List of environment detectors to be used in chain.
        If not set, default builtin chain is used.

    :param detectors_opts: Detectors options dictionary.
        Where keys are detector names and values are keyword arguments dicts.

    :param use_envfiles: Whether to set environment variables (if not already set)
        using data from .env files.

    """
    detectors_opts = detectors_opts or {}

    if detectors is None:
        detectors = DETECTORS.keys()

    env_type = None

    for detector in detectors:
        opts = detectors_opts.get(detector, {})
        detector = get_detector(detector)

        detector = detector(**opts)
        env_name = detector.probe()

        if env_name:
            env_type = get_type(env_name)
            break

    if env_type is None and default is not None:
        env_type = get_type(default)

    env = None

    if env_type is not None:
        env = env_type()
        use_envfiles and env.update_from_envfiles()

    return env


def import_by_environment(
        environment: Environment = None,
        module_name_pattern: str = 'settings_%s',
        silent: bool = False,
        package_name: str = None
) -> Optional[Environment]:
    """Automatically imports symbols of a submodule of a package for given
    (or detected) environment into globals of an entry-point submodule.

    Returns``Environment`` object if module is imported or ``None``.

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

    :param environment:

    :param module_name_pattern: Environment submodule name pattern.
        ``%s`` will be replaced with environment name.

    :param silent: If ``True`` no import error (if any) will be raised.

    :param package_name: Name of the package holding settings file.
        We'll try to guess it if not provided.

        E.g.:
            * someproject.settings
            * someproject.inner.settings

    """
    environment = environment or get_environment()

    module_name_pattern = f'.{module_name_pattern}'

    settings_module = currentframe().f_back
    filedir = dirname(settings_module.f_code.co_filename)

    if package_name is None:
        package_name = basename(filedir)

        if package_name not in sys.modules.keys():
            # Last try to deduce maybe 'someproject.settings'.
            package_name = f'{basename(dirname(filedir))}.{package_name}'

    result = None

    try:
        env_module = import_module(module_name_pattern % environment, package_name)
        settings_module.f_globals.update(env_module.__dict__)

        result = environment

    except (ImportError, SystemError):
        if not silent:
            raise

    return result
