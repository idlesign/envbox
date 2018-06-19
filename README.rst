envbox
======
https://github.com/idlesign/envbox

|release| |lic| |ci| |coverage|

.. |release| image:: https://img.shields.io/pypi/v/envbox.svg
    :target: https://pypi.python.org/pypi/envbox

.. |lic| image:: https://img.shields.io/pypi/l/envbox.svg
    :target: https://pypi.python.org/pypi/envbox

.. |ci| image:: https://img.shields.io/travis/idlesign/envbox/master.svg
    :target: https://travis-ci.org/idlesign/envbox

.. |coverage| image:: https://img.shields.io/coveralls/idlesign/envbox/master.svg
    :target: https://coveralls.io/r/idlesign/envbox


Description
-----------

*Detect environment type and work within.*


Features
~~~~~~~~

* Environment type detection (extendable system);
* Support for ``.env`` files;
* Convenient ``os.environ`` proxying (with optional values casting into Python natives);
* Automatic submodule-for-environment import tool;
* Cosy per-thread settings container with environment var support;
* CLI for environment probing.


Code sample
~~~~~~~~~~~

.. code-block:: python

    from envbox import get_environment

    # Detect current environment type
    # and get its object.
    #
    # Default detection sources:
    # 1. ``PYTHON_ENV`` env variable
    # 2. ``environment`` file contents
    #
    # By default this function will also try to read env variables from .env files.
    env = get_environment()

    env.name
    # >> development

    env.is_production
    # >> False

    env.get('HOME')
    # The same as env['HOME'] and env.HOME
    # >> /home/idle/

    env.getmany('PYTHON')
    # {'UNBUFFERED': '1', 'IOENCODING': 'UTF-8', 'PATH': ...}


Read the docs for more examples.

CLI
~~~

.. code-block:: bash

    $ envbox probe
    # >> Detected environment type: development (Development)

    $ envbox show
    # >> [...]
    # >> SHELL = /bin/bash
    # >> [...]


**Note:** ``envbox`` CLI requires ``click`` package available.


Documentation
-------------

http://envbox.readthedocs.org/
