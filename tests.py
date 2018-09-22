from math import isnan

import pytest
from hypothesis import (
    HealthCheck,
    assume,
    given,
    settings,
    strategies as st,
    unlimited,
)

from twelvefactor import UNSET, Config, ConfigError, config

try:
    from unittest.mock import Mock, call, patch
except ImportError:
    from mock import Mock, call, patch

TRUE_STRINGS = (
    "t",
    "T",
    "true",
    "True",
    "tRue",
    "TRue",
    "trUe",
    "TrUe",
    "tRUe",
    "TRUe",
    "truE",
    "TruE",
    "tRuE",
    "TRuE",
    "trUE",
    "TrUE",
    "tRUE",
    "TRUE",
    "on",
    "On",
    "oN",
    "ON",
    "ok",
    "Ok",
    "oK",
    "OK",
    "y",
    "Y",
    "yes",
    "Yes",
    "yEs",
    "YEs",
    "yeS",
    "YeS",
    "yES",
    "YES",
    "1",
)

TYPES = (int, str, bool, list, set, lambda x: x)


def anything(*args):
    stratergies = [
        st.none(),
        st.integers(),
        st.booleans(),
        st.text(),
        st.binary(),
        st.floats().filter(lambda x: not isnan(x)),
    ]

    stratergies.extend(args)

    return st.one_of(*stratergies)


def get_kwargs():
    kwargs = {
        "default": st.one_of(st.just(UNSET), anything()),
        "key": st.one_of(st.none(), st.text()),
        "type_": st.sampled_from(TYPES),
        "subtype": st.sampled_from(TYPES),
    }

    return st.fixed_dictionaries(kwargs)


class TestConfig(object):
    @settings(timeout=unlimited, suppress_health_check=[HealthCheck.too_slow])
    @given(st.one_of(st.none(), st.dictionaries(st.text(), st.text())))
    def test_init(self, environ):
        if environ is None:
            with patch("os.environ") as m:
                instance = Config()
                assert instance.environ == m
        else:
            instance = Config(environ=environ)
            assert instance.environ == environ

    @given(st.text())
    def test_parse(self, value):
        instance = Config(environ={})

        assert instance.parse(value) == value

    @given(st.one_of(st.text(), st.sampled_from(TRUE_STRINGS)))
    def test_parse_boolean(self, value):
        instance = Config(environ={})

        assert instance.parse(value, type_=bool) == (value in TRUE_STRINGS)

    @given(
        st.lists(
            st.text().filter(lambda x: x and "," not in x and " " not in x)
        ),
        st.sampled_from([list, set, tuple]),
        st.integers(0, 5),
    )
    def test_parse_list(self, value, type_, padding):
        instance = Config(environ={})

        results = [Mock() for v in value]

        calls = [call(v) for v in value]

        m = Mock(side_effect=results)

        seperator = " " * padding + "," + " " * padding

        result = instance.parse(seperator.join(value), type_=type_, subtype=m)

        assert result == type_(results)

        m.assert_has_calls(calls)

    @given(
        st.lists(
            st.one_of(
                st.text().filter(
                    lambda x: x and "," not in x and " " not in x
                ),
                st.sampled_from(TRUE_STRINGS),
            )
        )
    )
    def test_parse_subtypes(self, value):
        instance = Config(environ={})

        result = instance.parse(",".join(value), type_=list, subtype=bool)

        assert result == [v in TRUE_STRINGS for v in value]

    @given(st.text(), st.booleans(), st.lists(st.text()).map(tuple))
    def test_parse_other(self, value, error, args):
        instance = Config(environ={})

        m = Mock()

        if error:
            m.side_effect = ValueError(*args)

        if not error:
            assert instance.parse(value, type_=m) == m.return_value
        else:
            with pytest.raises(ConfigError) as e:
                instance.parse(value, type_=m)

            assert e.value.args == args

        m.assert_called_once_with(value)

    @given(
        st.dictionaries(st.text(), st.text()).filter(bool),
        st.text(),
        st.booleans(),
        get_kwargs(),
        st.booleans(),
        st.choices(),
    )
    def test_get(self, environ, key, error, kwargs, mapper, choice):
        assume(key not in environ)
        try:
            str(key)
        except Exception:
            assume(False)

        instance = Config(environ=environ)
        instance.parse = Mock()

        kwargs["key"] = key if error else choice(list(environ.keys()))

        if mapper:
            kwargs["mapper"] = Mock()

        if error and kwargs["default"] == UNSET:
            with pytest.raises(ConfigError) as err:
                instance.get(**kwargs)

            message = "Unknown environment variable: {0}".format(key)

            assert str(err.value) == message
        else:
            if error:
                rv = kwargs["default"]
            else:
                rv = instance.parse.return_value

            expected = rv if not mapper else kwargs["mapper"].return_value

            assert instance.get(**kwargs) == expected

            value = kwargs["default"] if error else environ[kwargs["key"]]

            if not error:
                instance.parse.assert_called_once_with(
                    value, kwargs["type_"], kwargs["subtype"]
                )

            if mapper:
                kwargs["mapper"].assert_called_once_with(rv)

    @given(st.dictionaries(st.text(), get_kwargs()), st.booleans())
    def test_call(self, schema, type_):
        instance = Config(environ={})

        return_value = {}
        side_effect = {}
        calls = []

        mock = Mock(side_effect=lambda key, **kwargs: side_effect[key])
        instance.get = mock

        for key, kwargs in schema.items():
            k = kwargs["key"]

            if k is None:
                del kwargs["key"]
                k = key

            call = kwargs.copy()
            call["key"] = k

            if type_:
                kwargs["type"] = kwargs.pop("type_")

            calls.append(call)
            side_effect.setdefault(k, Mock())
            return_value[key] = side_effect[k]

        original = schema.copy()

        assert instance(schema) == return_value
        assert schema == original

        for kwargs in calls:
            instance.get.assert_any_call(**kwargs)

        assert instance.get.call_count == len(schema)

    @given(st.dictionaries(st.text(), st.sampled_from(TYPES)))
    def test_call_simple(self, schema):
        instance = Config(environ={})

        return_value = {}
        side_effect = {}
        calls = []

        mock = Mock(side_effect=lambda key, **kwargs: side_effect[key])
        instance.get = mock

        for k, v in schema.items():
            calls.append({"key": k, "type_": v})
            side_effect.setdefault(k, Mock())
            return_value[k] = side_effect[k]

        original = schema.copy()

        assert instance(schema) == return_value
        assert schema == original

        for kwargs in calls:
            instance.get.assert_any_call(**kwargs)

        assert instance.get.call_count == len(schema)


def test_config():
    assert isinstance(config, Config)
