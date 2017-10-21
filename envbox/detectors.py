from __future__ import unicode_literals, absolute_import

from collections import OrderedDict
from os import environ

from .utils import string_types

DETECTORS = OrderedDict()


class Detector(object):

    name = 'dummy'
    source = None

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def probe(self):  # pragma: nocover
        raise NotImplementedError


class Environ(Detector):
    """Gets environment from OS environment variable."""

    name = 'environ'
    source = 'PYTHON_ENV'

    def probe(self):
        return environ.get(self.source)


class File(Detector):
    """Gets environment from file."""

    name = 'file'
    source = 'environment'

    def probe(self):
        env_name = None

        try:
            with open(self.source) as f:
                env_name = f.read().strip()

        except IOError:
            pass

        return env_name


def register_detector(detector):
    """Registers an environment detector.

    :param Detector detector:

    """
    DETECTORS[detector.name] = detector


def get_detector(cls_or_name):
    """Returns detector by alias (or class itself)

    :param Detector|str|unicode cls_or_name:

    :rtype: Detector

    """
    if isinstance(cls_or_name, string_types):
        return DETECTORS[cls_or_name]

    return cls_or_name


def __register_builtins():

    if DETECTORS:  # pragma: nocover
        return

    for cls in [Environ, File]:
        register_detector(cls)


__register_builtins()
