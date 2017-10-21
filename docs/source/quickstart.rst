Quickstart
==========


Basic usage
~~~~~~~~~~~

.. code-block:: python

    from envbox import get_environment

    # Let's detect current environment type and get its object.
    # * See and use `get_environment` function arguments to impose restrictions upon detection system.

    # Default detection sources:
    # 1. ``PYTHON_ENV`` env variable
    # 2. ``environment`` file contents
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


Environment type aliases
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from envbox import get_environment, PRODUCTION

    # Let's make `prod` string identify production environment.
    register_type(PRODUCTION, alias='prod')

    # Now if someone has used `prod`
    # we correctly identify it as production environment.
    get_environment().is_production  # True

