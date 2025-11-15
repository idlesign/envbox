from os import environ
from typing import Union, Type, Optional, Dict

DETECTORS: Dict[str, Type['Detector']] = {}


class Detector:

    name = 'dummy'
    source = None

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def probe(self) -> Optional[str]:  # pragma: nocover
        raise NotImplementedError


TypeDetectorArg = Union[Type[Detector], str]


class Environ(Detector):
    """Gets environment from OS environment variable."""

    name = 'environ'
    source = 'PYTHON_ENV'

    def probe(self) -> Optional[str]:
        return environ.get(self.source)


class File(Detector):
    """Gets environment from file."""

    name = 'file'
    source = 'environment'

    def probe(self) -> Optional[str]:
        env_name = None

        try:
            with open(self.source) as f:
                env_name = f.read().strip()

        except IOError:
            pass

        return env_name


def register_detector(detector: Type[Detector]):
    """Registers an environment detector.

    :param detector:

    """
    DETECTORS[detector.name] = detector


def get_detector(cls_or_name: TypeDetectorArg) -> Type[Detector]:
    """Returns detector by alias (or class itself)

    :param cls_or_name:

    """
    if isinstance(cls_or_name, str):
        return DETECTORS[cls_or_name]

    return cls_or_name


def __register_builtins():

    if DETECTORS:  # pragma: nocover
        return

    for cls in [Environ, File]:
        register_detector(cls)


__register_builtins()
