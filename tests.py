import math
import typing
import unittest.mock as mock

import hypothesis
import hypothesis.strategies as st
import pytest

import twelvefactor

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


def anything(
    *args: hypothesis.searchstrategy.SearchStrategy
) -> hypothesis.searchstrategy.SearchStrategy:
    stratergies: typing.List[hypothesis.searchstrategy.SearchStrategy] = [
        st.none(),
        st.integers(),
        st.booleans(),
        st.text(),
        st.binary(),
        st.floats().filter(lambda x: not math.isnan(x)),
    ]

    stratergies.extend(args)

    return st.one_of(*stratergies)


def get_kwargs() -> hypothesis.searchstrategy.SearchStrategy[typing.Dict]:
    kwargs = {
        "default": st.one_of(st.just(twelvefactor.UNSET), anything()),
        "key": st.one_of(st.none(), st.text()),
        "type_": st.sampled_from(TYPES),
        "subtype": st.sampled_from(TYPES),
    }

    return st.fixed_dictionaries(kwargs)


class TestConfig(object):
    @hypothesis.settings(  # type: ignore
        timeout=hypothesis.unlimited,
        suppress_health_check=[hypothesis.HealthCheck.too_slow],
    )
    @hypothesis.given(
        st.one_of(st.none(), st.dictionaries(st.text(), st.text()))
    )
    def test_init(self, environ: typing.Dict[str, str]) -> None:
        if environ is None:
            with mock.patch("os.environ") as m:
                instance = twelvefactor.Config()
                assert instance.environ == m
        else:
            instance = twelvefactor.Config(environ=environ)
            assert instance.environ == environ

    @hypothesis.given(st.text())
    def test_parse(self, value: str) -> None:
        instance = twelvefactor.Config(environ={})

        assert instance.parse(value) == value

    @hypothesis.given(st.one_of(st.text(), st.sampled_from(TRUE_STRINGS)))
    def test_parse_boolean(self, value: str) -> None:
        instance = twelvefactor.Config(environ={})

        assert instance.parse(value, type_=bool) == (value in TRUE_STRINGS)

    @hypothesis.given(
        st.lists(
            st.text().filter(
                lambda x: bool(x and "," not in x and " " not in x)
            )
        ),
        st.sampled_from([list, set, tuple]),
        st.integers(0, 5),
    )
    def test_parse_list(
        self, value: typing.List[str], type_: typing.Type, padding: int
    ) -> None:
        instance = twelvefactor.Config(environ={})

        results = [mock.Mock() for v in value]

        calls = [mock.call(v) for v in value]

        m = mock.Mock(side_effect=results)

        seperator = " " * padding + "," + " " * padding

        result = instance.parse(seperator.join(value), type_=type_, subtype=m)

        assert result == type_(results)

        m.assert_has_calls(calls)

    @hypothesis.given(
        st.lists(
            st.one_of(
                st.text().filter(
                    lambda x: bool(x and "," not in x and " " not in x)
                ),
                st.sampled_from(TRUE_STRINGS),
            )
        )
    )
    def test_parse_subtypes(self, value: str) -> None:
        instance = twelvefactor.Config(environ={})

        result = instance.parse(",".join(value), type_=list, subtype=bool)

        assert result == [v in TRUE_STRINGS for v in value]

    @hypothesis.given(st.text(), st.booleans(), st.lists(st.text()).map(tuple))
    def test_parse_other(
        self, value: str, error: bool, args: typing.Tuple[str, ...]
    ) -> None:
        instance = twelvefactor.Config(environ={})

        m = mock.Mock()

        if error:
            m.side_effect = ValueError(*args)

        if not error:
            assert instance.parse(value, type_=m) == m.return_value
        else:
            with pytest.raises(twelvefactor.ConfigError) as e:
                instance.parse(value, type_=m)

            assert e.value.args == args

        m.assert_called_once_with(value)

    @hypothesis.given(
        st.dictionaries(st.text(), st.text()).filter(bool),
        st.text(),
        st.booleans(),
        get_kwargs(),
        st.booleans(),
        st.data(),
    )
    def test_get(
        self,
        environ: typing.Dict[str, str],
        key: str,
        error: bool,
        kwargs: typing.Dict,
        mapper: bool,
        data: st.DataObject,
    ) -> None:
        hypothesis.assume(key not in environ)

        instance = twelvefactor.Config(environ=environ)
        instance.parse = mock.Mock()  # type: ignore

        kwargs["key"] = (
            key
            if error
            else data.draw(  # type: ignore
                st.sampled_from(list(environ.keys()))
            )
        )

        if mapper:
            kwargs["mapper"] = mock.Mock()

        if error and kwargs["default"] == twelvefactor.UNSET:
            with pytest.raises(twelvefactor.ConfigError) as err:
                instance.get(**kwargs)

            message = "Unknown environment variable: {0}".format(key)

            assert str(err.value) == message
        else:
            if error:
                rv = kwargs["default"]
            else:
                rv = typing.cast(mock.Mock, instance.parse).return_value

            expected = rv if not mapper else kwargs["mapper"].return_value

            assert instance.get(**kwargs) == expected

            value = kwargs["default"] if error else environ[kwargs["key"]]

            if not error:
                typing.cast(mock.Mock, instance.parse).assert_called_once_with(
                    value, kwargs["type_"], kwargs["subtype"]
                )

            if mapper:
                kwargs["mapper"].assert_called_once_with(rv)

    @hypothesis.given(st.dictionaries(st.text(), get_kwargs()))
    def test_call(self, schema: typing.Dict) -> None:
        instance = twelvefactor.Config(environ={})

        return_value = {}
        side_effect: typing.Dict[str, mock.Mock] = {}
        calls = []

        instance.get = mock.Mock(  # type: ignore
            side_effect=lambda key, **kwargs: side_effect[key]
        )

        for key, kwargs in schema.items():
            k = kwargs["key"]

            if k is None:
                del kwargs["key"]
                k = key

            call = kwargs.copy()
            call["key"] = k

            kwargs["type"] = kwargs.pop("type_")

            call.setdefault("default", twelvefactor.UNSET)
            call.setdefault("type_", str)
            call.setdefault("subtype", str)
            call.setdefault("mapper", None)

            print(kwargs)
            print(mock.call)

            calls.append(call)
            side_effect.setdefault(k, mock.Mock())
            return_value[key] = side_effect[k]

        original = schema.copy()

        assert instance(schema) == return_value
        assert schema == original

        for kwargs in calls:
            typing.cast(mock.Mock, instance.get).assert_any_call(**kwargs)

        assert typing.cast(mock.Mock, instance.get).call_count == len(schema)

    @hypothesis.given(st.dictionaries(st.text(), st.sampled_from(TYPES)))
    def test_call_simple(self, schema: typing.Dict) -> None:
        instance = twelvefactor.Config(environ={})

        return_value = {}
        side_effect: typing.Dict[str, mock.Mock] = {}
        calls = []

        instance.get = mock.Mock(  # type: ignore
            side_effect=lambda key, **kwargs: side_effect[key]
        )

        for k, v in schema.items():
            calls.append({"key": k, "type_": v})
            side_effect.setdefault(k, mock.Mock())
            return_value[k] = side_effect[k]

        original = schema.copy()

        assert instance(schema) == return_value
        assert schema == original

        for kwargs in calls:
            typing.cast(mock.Mock, instance.get).assert_any_call(**kwargs)

        assert typing.cast(mock.Mock, instance.get).call_count == len(schema)


def test_config() -> None:
    assert isinstance(twelvefactor.config, twelvefactor.Config)
