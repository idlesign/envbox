import os
import io
from setuptools import setup, find_packages
import sys

from envbox import VERSION


PATH_BASE = os.path.dirname(__file__)


def get_readme():
    # This will return README (including those with Unicode symbols).
    with io.open(os.path.join(PATH_BASE, 'README.rst')) as f:
        return f.read()


setup(
    name='envbox',
    version='.'.join(map(str, VERSION)),
    url='https://github.com/idlesign/envbox',

    description='Detect environment type and work within.',
    long_description=get_readme(),
    license='BSD 3-Clause License',

    author='Igor `idle sign` Starikov',
    author_email='idlesign@yandex.ru',

    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,

    install_requires=[],
    setup_requires=[] + (['pytest-runner'] if 'test' in sys.argv else []) + [],
    extras_require={
        'cli': ['click>=2.0'],
    },

    entry_points={
        'console_scripts': ['envbox = envbox.cli:main'],
    },

    test_suite='tests',
    tests_require=[
        'pytest',
        'pytest-datafixtures>=1.0.0',
    ],

    classifiers=[
        # As in https://pypi.python.org/pypi?:action=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: BSD License'
    ],
)


