import sys


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
