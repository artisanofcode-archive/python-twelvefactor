[![Status](https://img.shields.io/travis/artisanofcode/python-twelvefactor.svg?style=flat-square)](https://travis-ci.org/artisanofcode/python-twelvefactor)
[![PyPi](https://img.shields.io/pypi/v/twelvefactor.svg?style=flat-square)](https://pypi.python.org/pypi/twelvefactor/) 
[![Python 3.6+](https://img.shields.io/pypi/pyversions/twelvefactor.svg?style=flat-square)](https://www.python.org/download/releases/3.6.0/) 
[![MIT](https://img.shields.io/github/license/artisanofcode/python-twelvefactor.svg?style=flat-square)](http://dan.mit-license.org/)

# twelvefactor

Utilities for creating a [12 factor](http://12factor.net/) application, at 
present it allows you to parse the processes environment variables into a 
configuration dictionary.

For more information check the [Documentation](http://twelvefactor.craftedbyartisans.com/).

## Installing

Install using pip

```shell
pip install twelvefactor
```

Install using [poetry]()

```shell
poetry add twelvefactor
```

## Example

###  Flask

```python
import flask
import twelvefactor

SCHEMA = {
    'DEBUG': {
        'type': bool,
        'default': False,
    },
    'SECRET_KEY': str,
}

app = flask.Flask()
app.config.update(twelvefactor.config(SCHEMA))
```

### Django

```python
# settings.py
import dj_database_url
import twelvefactor

SCHEMA = {
    "DEBUG": {"type": bool, "default": False},
    "SECRET_KEY": str,
    "DATABASES": {
        "key": "DATABASE_URL",
        "default": "sqlite:///",
        "mapper": lambda v: {"default": dj_database_url.parse(v)},
    },
}

globals().update(twelvefactor.config(SCHEMA))
```

## Source

To install from source:

```shell
pip install poetry
git clone git://github.com/artisanofcode/python-twelvefactor.git
cd python-twelvefactor
poetry develop
```

## Release
  
  Update `CHANGES` and then run the following

```shell
poetry version patch
git commit -am 'bumped the version'
git tag v${VERSION}
poetry version prerelease
git commit -am 'prerelease version'
git push --tags
````

## History 

See [CHANGES](CHANGES)

## Licence

This project is licensed under the [MIT licence](http://dan.mit-license.org/).

## Meta

This project uses [Semantic Versioning](http://semver.org/).