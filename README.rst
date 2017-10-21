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


**Work in progress. Stay tuned.**


Description
-----------

*Detect environment type and work within.*


Features
~~~~~~~~

* Environment type detection (extendable system);
* Convenient ``os.environ`` proxying.


Code sample
~~~~~~~~~~~

.. code-block:: python

    from envbox import get_environment

    # Detect current environment type
    # and get its object.

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



Documentation
-------------

http://envbox.readthedocs.org/


