Schema
======

Example
-------

.. code-block:: python

    {
        'DEBUG': {
            'type': bool,
            'default': False,
        },
        'SECRET_KEY': str,
        'DATABASE': {
            'key': 'DATABASE_URL',
            'mapper': dj_database_url.parse
        },
        'SOME_SET': {
            'type': set,
            'subtype': int
        }
    }


Properties
----------

key
~~~

The name of the environment variable to look up, this allows you map map values
in the environment to differently named configuration variables, it defaults
to the name of the configuration variable.

default
~~~~~~~

A value to use should no environment variable be found, if no default is 
provided then an error will be thrown.

type
~~~~

A function to convert the string value to the correct type.

When :class:`list`, :class:`tuple`, or :class:`set` are provided then the value
will be interpreted as a comma separated list and interpreted based on the
subtype setting.

If no type is set then :class:`str` is assumed.

subtype
~~~~~~~

A function to convert the string sub-value to the correct type.

If no subtype is set then :class:`str` is assumed.

mapper
~~~~~~

A method to post process the value after it has been converted to the correct
type, it is the last transformation to be applied and should take the value and
transform it into a more suitable configuration value.

A mapper should not be used to instantiate complex classes such as database
adapters, these should be instantiated outside of the configuration code.

If no mapper is provided then the value is returned as is.

Shorthand
---------

When only a type is required you can specify a callable instead of a dictionary
defining the config value.

The following two examples are identical

.. code-block:: python

    {
        'DEBUG': bool
    }

.. code-block:: python

    {
        'DEBUG': {
            'type': bool
        }
    }
