from os import environ
from pathlib import Path

DETECTORS: dict[str, type['Detector']] = {}


class Detector:

    name = 'dummy'
    source = None

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def probe(self) -> str | None:  # pragma: nocover
        raise NotImplementedError


TypeDetectorArg = type[Detector] | str


class Environ(Detector):
    """Gets environment from OS environment variable."""

    name = 'environ'
    source = 'PYTHON_ENV'

    def probe(self) -> str | None:
        return environ.get(self.source)


class File(Detector):
    """Gets environment from file."""

    name = 'file'
    source = 'environment'

    def probe(self) -> str | None:
        env_name = None

        try:
            with Path(self.source).open() as f:
                env_name = f.read().strip()

        except OSError:
            pass

        return env_name


def register_detector(detector: type[Detector]):
    """Registers an environment detector.

    :param detector:

    """
    DETECTORS[detector.name] = detector


def get_detector(cls_or_name: TypeDetectorArg) -> type[Detector]:
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
