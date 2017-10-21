from .detectors import DETECTORS, get_detector
from .envs import EnvironmentType, DEVELOPMENT, get_type


def get_environment(default=DEVELOPMENT, detectors=None, detectors_opts=None):
    """Returns current environment type object.

    :param str|EnvironmentType default: Default environment type or alias.

    :param list[Detector] detectors: List of environment detectors to be used in chain.
        If not set, default builtin chain is used.

    :param dict detectors_opts: Detectors options dictionary.
        Where keys are detector names and values are keyword arguments dicts.

    :rtype: EnvironmentType
    """
    detectors_opts = detectors_opts or {}

    if detectors is None:
        detectors = DETECTORS.keys()

    env = None

    for detector in detectors:
        opts = detectors_opts.get(detector, {})
        detector = get_detector(detector)

        detector = detector(**opts)
        env = detector.probe()

        if env:
            env = get_type(env)()
            break

    if env is None:
        env = get_type(default)

    return env
