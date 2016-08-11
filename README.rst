twelvefactor
============

Utilities for creating a `12 factor`_ application, at present it allows you to 
parse the processes environment variables into a configuration dictionary.

For more information check the Documentation_.

Example
-------

.. code:: python

    from twelvefactor import config

    globals().update(config({
        'DEBUG': {
            'type': bool,
            'default': False,
        },
        'SECRET_KEY': str,
    }))

    print(DEBUG)

Install
-------

To install twelvefactor via pip:

::

    pip install twelvefactor

Source
------

To install from source:

::

    git clone git://github.com/artisanofcode/python-twelvefactor.git
    cd python-twelvefactor
    python setup.py develop


History
-------

See `CHANGES <CHANGES>`_

Licence
-------

This project is licensed under the `MIT licence`_.

Meta
----

This project uses `Semantic Versioning`_.

.. _12 factor: http://12factor.net/
.. _Documentation: http://twelvefactor.readthedocs.io/
.. _Semantic Versioning: http://semver.org/
.. _MIT Licence: http://dan.mit-license.org/