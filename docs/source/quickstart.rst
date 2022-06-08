Quickstart
==========


Basic usage
-----------

.. code-block:: python

    from envbox import get_environment

    # Let's detect current environment type and get its object.
    # * See and use `get_environment` function arguments to impose restrictions upon detection system.
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

    # We can also try to cast env values into Python natives.
    env.getmany_casted('PYTHON')
    # Note that `UNBUFFERED` is int now.
    # {'UNBUFFERED': 1, 'IOENCODING': 'UTF-8', 'PATH': ...}


.env files as a source
----------------------

You may want to put your environment vars into ``.env`` files
(e.g.: ``.env``, ``.env.development`` ``.env.production``)
to be read by ``envbox``::

    MY_VAR_1 = value1
    HOME = /home/other/

    # comments are ignored, just as lines without definitions

    # mathing quotes (" and ') are stripped
    MY_QUOTED = "some quoted "

    # ${VARNAME} will be replaced by value from env (if available)
    MY_VAR_2 = ${MY_QUOTED}

    # multiline with dangling quotes
    MULTI_1 = "
    line1
    line2
    "

    # multiline classic
    MULTI_2 = "line1
    line2
    line3"

    # multiline as one line
    MULTI_3 = "one\ntwo"


``envbox`` will try to load such files from the current working directory
for the current environment type automatically.


Settings container
------------------

If you need a per-thread settings storage you can do the following:

.. code-block:: python

    # Somewhere in your setting module declare settings:
    class _Settings(SettingsBase):

        ONE = 1
        SOME = 'two'
        ANOTHER = True

    Settings = _Settings()


    # Now access those settings from other modules(s).
    if Settings.ANOTHER:
        Settings.SOME = 'three'


Accessing any setting which was not set in the session, will lead to appropriate environment variable probing.



Environment type aliases
------------------------

.. code-block:: python

    from envbox import get_environment, PRODUCTION

    # Let's make `prod` string identify production environment.
    register_type(PRODUCTION, alias='prod')

    # Now if someone has used `prod`
    # we correctly identify it as production environment.
    get_environment().is_production  # True



Automatic submodule import
--------------------------

**envbox** features ``import_by_environment()`` function which automatically imports symbols of a submodule
of a package for the given (or detected) environment into globals of an entry-point submodule.

.. note:: This could be useful not only for Django-projects where submodule-based settings definition is rather usual
  but also for various other cases.


Example::

    - project
    --- __init__.py
    --- settings.py
    --- settings_development.py

1. Here ``project`` is a package available for import (note ``__init__.py``).

2. ``settings.py`` is an entry point module for settings using ``import_by_environment()``.

    .. code-block:: python

        from envbox import import_by_environment


        current_env = import_by_environment()

        print(f'Environment type: {current_env}')


3. ``settings_development.py`` is one of module files for certain environment (development).

4. ``import_by_environment()`` call in ``settings.py`` makes symbols from ``settings_development.py``
   available from ``settings.py``.

