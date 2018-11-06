import cmath
import itertools
import math
import typing
import unittest.mock as mock

import hypothesis
import hypothesis.strategies as st
import pytest

import twelvefactor

# Generate all possible case permutations of the strings in TRUE_STRINGS
TRUE_STRINGS = [
    v
    for s in twelvefactor.Config.TRUE_STRINGS
    for v in map(
        "".join, itertools.product(*((c.upper(), c.lower()) for c in s))
    )
]


@hypothesis.given(
    key=st.shared(st.text(), "key"),
    value=st.shared(st.sampled_from(TRUE_STRINGS), "value"),
    environ=st.tuples(
        st.dictionaries(keys=st.text(), values=st.text()),
        st.shared(st.text(), "key"),
        st.shared(st.sampled_from(TRUE_STRINGS), "value"),
    ).map(lambda x: dict(x[0], **{x[1]: str(x[2])})),
)
def test_it_should_be_able_to_get_true(
    key: str, value: bool, environ: typing.Dict[str, str]
) -> None:
    config = twelvefactor.Config(environ=environ)

    assert config.get(key=key, type_=bool)


@hypothesis.given(
    key=st.shared(st.text(), "key"),
    value=st.shared(
        st.text().filter(lambda x: x not in TRUE_STRINGS), "value"
    ),
    environ=st.tuples(
        st.dictionaries(keys=st.text(), values=st.text()),
        st.shared(st.text(), "key"),
        st.shared(st.text().filter(lambda x: x not in TRUE_STRINGS), "value"),
    ).map(lambda x: dict(x[0], **{x[1]: str(x[2])})),
)
def test_it_should_be_able_to_get_false(
    key: str, value: bool, environ: typing.Dict[str, str]
) -> None:
    config = twelvefactor.Config(environ=environ)

    assert not config.get(key=key, type_=bool)


@hypothesis.given(
    key=st.shared(st.text(), "key"),
    value=st.shared(st.text(), "value"),
    environ=st.tuples(
        st.dictionaries(keys=st.text(), values=st.text()),
        st.shared(st.text(), "key"),
        st.shared(st.text(), "value"),
    ).map(lambda x: dict(x[0], **{x[1]: str(x[2])})),
)
def test_it_should_be_able_to_get_strings(
    key: str, value: str, environ: typing.Dict[str, str]
) -> None:
    config = twelvefactor.Config(environ=environ)

    assert config.get(key=key) == value


@hypothesis.given(
    key=st.shared(st.text(), "key"),
    value=st.shared(st.integers(), "value"),
    environ=st.tuples(
        st.dictionaries(keys=st.text(), values=st.text()),
        st.shared(st.text(), "key"),
        st.shared(st.integers(), "value"),
    ).map(lambda x: dict(x[0], **{x[1]: str(x[2])})),
)
def test_it_should_be_able_to_get_integers(
    key: str, value: int, environ: typing.Dict[str, str]
) -> None:
    config = twelvefactor.Config(environ=environ)

    assert config.get(key=key, type_=int) == value


@hypothesis.given(
    key=st.shared(st.text(), "key"),
    value=st.shared(st.floats(), "value"),
    environ=st.tuples(
        st.dictionaries(keys=st.text(), values=st.text()),
        st.shared(st.text(), "key"),
        st.shared(st.floats(), "value"),
    ).map(lambda x: dict(x[0], **{x[1]: str(x[2])})),
)
def test_it_should_be_able_to_get_floats(
    key: str, value: float, environ: typing.Dict[str, str]
) -> None:
    config = twelvefactor.Config(environ=environ)

    result = typing.cast(float, config.get(key=key, type_=float))

    if math.isnan(value):
        assert math.isnan(result)
    else:
        assert result == value


@hypothesis.given(
    key=st.shared(st.text(), "key"),
    value=st.shared(st.complex_numbers(), "value"),
    environ=st.tuples(
        st.dictionaries(keys=st.text(), values=st.text()),
        st.shared(st.text(), "key"),
        st.shared(st.complex_numbers(), "value"),
    ).map(lambda x: dict(x[0], **{x[1]: str(x[2])})),
)
def test_it_should_be_able_to_get_complex_numbers(
    key: str, value: complex, environ: typing.Dict[str, str]
) -> None:
    config = twelvefactor.Config(environ=environ)

    result = typing.cast(complex, config.get(key=key, type_=complex))

    if cmath.isnan(value):
        assert cmath.isnan(result)
    else:
        assert result == value


@hypothesis.given(
    key=st.shared(st.text(), "key"),
    value=st.shared(st.lists(elements=st.booleans()), "value"),
    environ=st.tuples(
        st.dictionaries(keys=st.text(), values=st.text()),
        st.shared(st.text(), "key"),
        st.shared(st.lists(elements=st.booleans()), "value").map(
            lambda x: ",".join(str(v) for v in x)
        ),
    ).map(lambda x: dict(x[0], **{x[1]: str(x[2])})),
)
def test_it_should_be_able_to_get_boolean_list(
    key: str, value: typing.List[bool], environ: typing.Dict[str, str]
) -> None:
    config = twelvefactor.Config(environ=environ)

    result = config.get(key=key, type_=list, subtype=bool)

    assert result == value


@hypothesis.given(
    key=st.shared(st.text(), "key"),
    value=st.shared(
        st.lists(elements=st.booleans()).map(lambda x: tuple(x)), "value"
    ),
    environ=st.tuples(
        st.dictionaries(keys=st.text(), values=st.text()),
        st.shared(st.text(), "key"),
        st.shared(
            st.lists(elements=st.booleans()).map(lambda x: tuple(x)), "value"
        ).map(lambda x: ",".join(str(v) for v in x)),
    ).map(lambda x: dict(x[0], **{x[1]: str(x[2])})),
)
def test_it_should_be_able_to_get_boolean_tuple(
    key: str, value: typing.Tuple[bool, ...], environ: typing.Dict[str, str]
) -> None:
    config = twelvefactor.Config(environ=environ)

    result = config.get(key=key, type_=tuple, subtype=bool)

    assert result == value


@hypothesis.given(
    key=st.shared(st.text(), "key"),
    value=st.shared(
        st.lists(elements=st.booleans()).map(lambda x: set(x)), "value"
    ),
    environ=st.tuples(
        st.dictionaries(keys=st.text(), values=st.text()),
        st.shared(st.text(), "key"),
        st.shared(
            st.lists(elements=st.booleans()).map(lambda x: set(x)), "value"
        ).map(lambda x: ",".join(str(v) for v in x)),
    ).map(lambda x: dict(x[0], **{x[1]: str(x[2])})),
)
def test_it_should_be_able_to_get_boolean_set(
    key: str, value: typing.Set[bool], environ: typing.Dict[str, str]
) -> None:
    config = twelvefactor.Config(environ=environ)

    result = config.get(key=key, type_=set, subtype=bool)

    assert result == value


@hypothesis.given(
    key=st.shared(st.text(), "key"),
    value=st.shared(
        st.lists(elements=st.booleans()).map(lambda x: frozenset(x)), "value"
    ),
    environ=st.tuples(
        st.dictionaries(keys=st.text(), values=st.text()),
        st.shared(st.text(), "key"),
        st.shared(
            st.lists(elements=st.booleans()).map(lambda x: frozenset(x)),
            "value",
        ).map(lambda x: ",".join(str(v) for v in x)),
    ).map(lambda x: dict(x[0], **{x[1]: str(x[2])})),
)
def test_it_should_be_able_to_get_boolean_frozenset(
    key: str, value: typing.FrozenSet[bool], environ: typing.Dict[str, str]
) -> None:
    config = twelvefactor.Config(environ=environ)

    result = config.get(key=key, type_=frozenset, subtype=bool)

    assert result == value


@hypothesis.given(
    key=st.shared(st.text(), "key"),
    value=st.shared(st.lists(elements=st.integers()), "value"),
    environ=st.tuples(
        st.dictionaries(keys=st.text(), values=st.text()),
        st.shared(st.text(), "key"),
        st.shared(st.lists(elements=st.integers()), "value").map(
            lambda x: ",".join(str(v) for v in x)
        ),
    ).map(lambda x: dict(x[0], **{x[1]: str(x[2])})),
)
def test_it_should_be_able_to_get_integer_list(
    key: str, value: typing.List[int], environ: typing.Dict[str, str]
) -> None:
    config = twelvefactor.Config(environ=environ)

    result = config.get(key=key, type_=list, subtype=int)

    assert result == value


@hypothesis.given(
    key=st.shared(st.text(), "key"),
    value=st.shared(
        st.lists(elements=st.integers()).map(lambda x: tuple(x)), "value"
    ),
    environ=st.tuples(
        st.dictionaries(keys=st.text(), values=st.text()),
        st.shared(st.text(), "key"),
        st.shared(
            st.lists(elements=st.integers()).map(lambda x: tuple(x)), "value"
        ).map(lambda x: ",".join(str(v) for v in x)),
    ).map(lambda x: dict(x[0], **{x[1]: str(x[2])})),
)
def test_it_should_be_able_to_get_integer_tuple(
    key: str, value: typing.Tuple[int, ...], environ: typing.Dict[str, str]
) -> None:
    config = twelvefactor.Config(environ=environ)

    result = config.get(key=key, type_=tuple, subtype=int)

    assert result == value


@hypothesis.given(
    key=st.shared(st.text(), "key"),
    value=st.shared(
        st.lists(elements=st.integers()).map(lambda x: set(x)), "value"
    ),
    environ=st.tuples(
        st.dictionaries(keys=st.text(), values=st.text()),
        st.shared(st.text(), "key"),
        st.shared(
            st.lists(elements=st.integers()).map(lambda x: set(x)), "value"
        ).map(lambda x: ",".join(str(v) for v in x)),
    ).map(lambda x: dict(x[0], **{x[1]: str(x[2])})),
)
def test_it_should_be_able_to_get_integer_set(
    key: str, value: typing.Set[int], environ: typing.Dict[str, str]
) -> None:
    config = twelvefactor.Config(environ=environ)

    result = config.get(key=key, type_=set, subtype=int)

    assert result == value


@hypothesis.given(
    key=st.shared(st.text(), "key"),
    value=st.shared(
        st.lists(elements=st.integers()).map(lambda x: frozenset(x)), "value"
    ),
    environ=st.tuples(
        st.dictionaries(keys=st.text(), values=st.text()),
        st.shared(st.text(), "key"),
        st.shared(
            st.lists(elements=st.integers()).map(lambda x: frozenset(x)),
            "value",
        ).map(lambda x: ",".join(str(v) for v in x)),
    ).map(lambda x: dict(x[0], **{x[1]: str(x[2])})),
)
def test_it_should_be_able_to_get_integer_frozenset(
    key: str, value: typing.FrozenSet[int], environ: typing.Dict[str, str]
) -> None:
    config = twelvefactor.Config(environ=environ)

    result = config.get(key=key, type_=frozenset, subtype=int)

    assert result == value


@hypothesis.given(
    key=st.shared(st.text(), "key"),
    value=st.shared(st.lists(elements=st.floats(allow_nan=False)), "value"),
    environ=st.tuples(
        st.dictionaries(keys=st.text(), values=st.text()),
        st.shared(st.text(), "key"),
        st.shared(st.lists(elements=st.floats(allow_nan=False)), "value").map(
            lambda x: ",".join(str(v) for v in x)
        ),
    ).map(lambda x: dict(x[0], **{x[1]: str(x[2])})),
)
def test_it_should_be_able_to_get_float_list(
    key: str, value: typing.List[float], environ: typing.Dict[str, str]
) -> None:
    config = twelvefactor.Config(environ=environ)

    result = config.get(key=key, type_=list, subtype=float)

    assert result == value


@hypothesis.given(
    key=st.shared(st.text(), "key"),
    value=st.shared(
        st.lists(elements=st.floats(allow_nan=False)).map(lambda x: tuple(x)),
        "value",
    ),
    environ=st.tuples(
        st.dictionaries(keys=st.text(), values=st.text()),
        st.shared(st.text(), "key"),
        st.shared(
            st.lists(elements=st.floats(allow_nan=False)).map(
                lambda x: tuple(x)
            ),
            "value",
        ).map(lambda x: ",".join(str(v) for v in x)),
    ).map(lambda x: dict(x[0], **{x[1]: str(x[2])})),
)
def test_it_should_be_able_to_get_float_tuple(
    key: str, value: typing.Tuple[float, ...], environ: typing.Dict[str, str]
) -> None:
    config = twelvefactor.Config(environ=environ)

    result = config.get(key=key, type_=tuple, subtype=float)

    assert result == value


@hypothesis.given(
    key=st.shared(st.text(), "key"),
    value=st.shared(
        st.lists(elements=st.floats(allow_nan=False)).map(lambda x: set(x)),
        "value",
    ),
    environ=st.tuples(
        st.dictionaries(keys=st.text(), values=st.text()),
        st.shared(st.text(), "key"),
        st.shared(
            st.lists(elements=st.floats(allow_nan=False)).map(
                lambda x: set(x)
            ),
            "value",
        ).map(lambda x: ",".join(str(v) for v in x)),
    ).map(lambda x: dict(x[0], **{x[1]: str(x[2])})),
)
def test_it_should_be_able_to_get_float_set(
    key: str, value: typing.Set[float], environ: typing.Dict[str, str]
) -> None:
    config = twelvefactor.Config(environ=environ)

    result = config.get(key=key, type_=set, subtype=float)

    assert result == value


@hypothesis.given(
    key=st.shared(st.text(), "key"),
    value=st.shared(
        st.lists(elements=st.floats(allow_nan=False)).map(
            lambda x: frozenset(x)
        ),
        "value",
    ),
    environ=st.tuples(
        st.dictionaries(keys=st.text(), values=st.text()),
        st.shared(st.text(), "key"),
        st.shared(
            st.lists(elements=st.floats(allow_nan=False)).map(
                lambda x: frozenset(x)
            ),
            "value",
        ).map(lambda x: ",".join(str(v) for v in x)),
    ).map(lambda x: dict(x[0], **{x[1]: str(x[2])})),
)
def test_it_should_be_able_to_get_float_frozenset(
    key: str, value: typing.FrozenSet[float], environ: typing.Dict[str, str]
) -> None:
    config = twelvefactor.Config(environ=environ)

    result = config.get(key=key, type_=frozenset, subtype=float)

    assert result == value


@hypothesis.given(
    key=st.shared(st.text(), "key"),
    value=st.shared(
        st.lists(elements=st.complex_numbers(allow_nan=False)), "value"
    ),
    environ=st.tuples(
        st.dictionaries(keys=st.text(), values=st.text()),
        st.shared(st.text(), "key"),
        st.shared(
            st.lists(elements=st.complex_numbers(allow_nan=False)), "value"
        ).map(lambda x: ",".join(str(v) for v in x)),
    ).map(lambda x: dict(x[0], **{x[1]: str(x[2])})),
)
def test_it_should_be_able_to_get_complex_number_list(
    key: str, value: typing.List[str], environ: typing.Dict[str, str]
) -> None:
    config = twelvefactor.Config(environ=environ)

    result = config.get(key=key, type_=list, subtype=complex)

    assert result == value


@hypothesis.given(
    key=st.shared(st.text(), "key"),
    value=st.shared(
        st.lists(elements=st.complex_numbers(allow_nan=False)).map(
            lambda x: tuple(x)
        ),
        "value",
    ),
    environ=st.tuples(
        st.dictionaries(keys=st.text(), values=st.text()),
        st.shared(st.text(), "key"),
        st.shared(
            st.lists(elements=st.complex_numbers(allow_nan=False)).map(
                lambda x: tuple(x)
            ),
            "value",
        ).map(lambda x: ",".join(str(v) for v in x)),
    ).map(lambda x: dict(x[0], **{x[1]: str(x[2])})),
)
def test_it_should_be_able_to_get_complex_number_tuple(
    key: str, value: typing.Tuple[complex, ...], environ: typing.Dict[str, str]
) -> None:
    config = twelvefactor.Config(environ=environ)

    result = config.get(key=key, type_=tuple, subtype=complex)

    assert result == value


@hypothesis.given(
    key=st.shared(st.text(), "key"),
    value=st.shared(
        st.lists(elements=st.complex_numbers(allow_nan=False)).map(
            lambda x: set(x)
        ),
        "value",
    ),
    environ=st.tuples(
        st.dictionaries(keys=st.text(), values=st.text()),
        st.shared(st.text(), "key"),
        st.shared(
            st.lists(elements=st.complex_numbers(allow_nan=False)).map(
                lambda x: set(x)
            ),
            "value",
        ).map(lambda x: ",".join(str(v) for v in x)),
    ).map(lambda x: dict(x[0], **{x[1]: str(x[2])})),
)
def test_it_should_be_able_to_get_complex_number_set(
    key: str, value: typing.Set[complex], environ: typing.Dict[str, str]
) -> None:
    config = twelvefactor.Config(environ=environ)

    result = config.get(key=key, type_=set, subtype=complex)

    assert result == value


@hypothesis.given(
    key=st.shared(st.text(), "key"),
    value=st.shared(
        st.lists(elements=st.complex_numbers(allow_nan=False)).map(
            lambda x: frozenset(x)
        ),
        "value",
    ),
    environ=st.tuples(
        st.dictionaries(keys=st.text(), values=st.text()),
        st.shared(st.text(), "key"),
        st.shared(
            st.lists(elements=st.complex_numbers(allow_nan=False)).map(
                lambda x: frozenset(x)
            ),
            "value",
        ).map(lambda x: ",".join(str(v) for v in x)),
    ).map(lambda x: dict(x[0], **{x[1]: str(x[2])})),
)
def test_it_should_be_able_to_get_complex_number_frozenset(
    key: str, value: typing.FrozenSet[complex], environ: typing.Dict[str, str]
) -> None:
    config = twelvefactor.Config(environ=environ)

    result = config.get(key=key, type_=frozenset, subtype=complex)

    assert result == value


@hypothesis.given(
    key=st.shared(st.text(), "key"),
    value=st.shared(
        st.lists(
            elements=st.text().filter(
                lambda x: "," not in x
                and x.strip(" ") == x
                and bool(x.strip(" "))
            )
        ),
        "value",
    ),
    environ=st.tuples(
        st.dictionaries(keys=st.text(), values=st.text()),
        st.shared(st.text(), "key"),
        st.shared(
            st.lists(
                elements=st.text().filter(
                    lambda x: "," not in x
                    and x.strip(" ") == x
                    and bool(x.strip(" "))
                )
            ),
            "value",
        ).map(",".join),
    ).map(lambda x: dict(x[0], **{x[1]: str(x[2])})),
)
def test_it_should_be_able_to_get_string_list(
    key: str, value: typing.List[str], environ: typing.Dict[str, str]
) -> None:
    config = twelvefactor.Config(environ=environ)

    result = config.get(key=key, type_=list)

    assert result == value


@hypothesis.given(
    key=st.shared(st.text(), "key"),
    value=st.shared(
        st.lists(
            elements=st.text().filter(
                lambda x: "," not in x
                and x.strip(" ") == x
                and bool(x.strip(" "))
            )
        ).map(lambda x: tuple(x)),
        "value",
    ),
    environ=st.tuples(
        st.dictionaries(keys=st.text(), values=st.text()),
        st.shared(st.text(), "key"),
        st.shared(
            st.lists(
                elements=st.text().filter(
                    lambda x: "," not in x
                    and x.strip(" ") == x
                    and bool(x.strip(" "))
                )
            ).map(lambda x: tuple(x)),
            "value",
        ).map(",".join),
    ).map(lambda x: dict(x[0], **{x[1]: str(x[2])})),
)
def test_it_should_be_able_to_get_string_tuple(
    key: str, value: typing.Tuple[str, ...], environ: typing.Dict[str, str]
) -> None:
    config = twelvefactor.Config(environ=environ)

    result = config.get(key=key, type_=tuple)

    assert result == value


@hypothesis.given(
    key=st.shared(st.text(), "key"),
    value=st.shared(
        st.lists(
            elements=st.text().filter(
                lambda x: "," not in x
                and x.strip(" ") == x
                and bool(x.strip(" "))
            )
        ).map(lambda x: set(x)),
        "value",
    ),
    environ=st.tuples(
        st.dictionaries(keys=st.text(), values=st.text()),
        st.shared(st.text(), "key"),
        st.shared(
            st.lists(
                elements=st.text().filter(
                    lambda x: "," not in x
                    and x.strip(" ") == x
                    and bool(x.strip(" "))
                )
            ).map(lambda x: set(x)),
            "value",
        ).map(",".join),
    ).map(lambda x: dict(x[0], **{x[1]: str(x[2])})),
)
def test_it_should_be_able_to_get_string_set(
    key: str, value: typing.Set[str], environ: typing.Dict[str, str]
) -> None:
    config = twelvefactor.Config(environ=environ)

    result = config.get(key=key, type_=set)

    assert result == value


@hypothesis.given(
    key=st.shared(st.text(), "key"),
    value=st.shared(
        st.lists(
            elements=st.text().filter(
                lambda x: "," not in x
                and x.strip(" ") == x
                and bool(x.strip(" "))
            )
        ).map(lambda x: frozenset(x)),
        "value",
    ),
    environ=st.tuples(
        st.dictionaries(keys=st.text(), values=st.text()),
        st.shared(st.text(), "key"),
        st.shared(
            st.lists(
                elements=st.text().filter(
                    lambda x: "," not in x
                    and x.strip(" ") == x
                    and bool(x.strip(" "))
                )
            ).map(lambda x: frozenset(x)),
            "value",
        ).map(",".join),
    ).map(lambda x: dict(x[0], **{x[1]: str(x[2])})),
)
def test_it_should_be_able_to_get_string_frozenset(
    key: str, value: typing.FrozenSet[str], environ: typing.Dict[str, str]
) -> None:
    config = twelvefactor.Config(environ=environ)

    result = config.get(key=key, type_=frozenset)

    assert result == value


@hypothesis.given(
    key=st.shared(st.text(), "key"),
    value=st.shared(st.text(), "value"),
    environ=st.tuples(
        st.dictionaries(keys=st.text(), values=st.text()),
        st.shared(st.text(), "key"),
        st.shared(st.text(), "value"),
    ).map(lambda x: dict(x[0], **{x[1]: str(x[2])})),
)
def test_it_should_be_apply_a_mapper_function(
    key: str, value: str, environ: typing.Dict[str, str]
) -> None:
    config = twelvefactor.Config(environ=environ)

    mapper = mock.Mock()

    assert config.get(key=key, mapper=mapper) == mapper.return_value

    mapper.assert_called_once_with(value)


@hypothesis.given(
    key=st.shared(st.text(), "key"),
    default=st.integers(),
    environ=st.tuples(
        st.dictionaries(keys=st.text(), values=st.text()),
        st.shared(st.text(), "key"),
    ).map(lambda x: {k: v for k, v in x[0].items() if k != x[1]}),
)
def test_it_should_return_default_when_not_found(
    key: str, default: int, environ: typing.Dict[str, str]
) -> None:
    config = twelvefactor.Config(environ=environ)

    assert config.get(key=key, type_=int, default=default) == default


@hypothesis.given(
    key=st.shared(st.text(), "key"),
    value=st.shared(st.text(), "value"),
    default=st.text(),
    environ=st.tuples(
        st.dictionaries(keys=st.text(), values=st.text()),
        st.shared(st.text(), "key"),
        st.shared(st.text(), "value"),
    ).map(lambda x: dict(x[0], **{x[1]: str(x[2])})),
)
def test_it_should_ignore_default_when_not_found(
    key: str, value: str, default: int, environ: typing.Dict[str, str]
) -> None:
    config = twelvefactor.Config(environ=environ)

    assert config.get(key=key, default=default) == value


@hypothesis.given(
    key=st.shared(st.text(), "key"),
    environ=st.tuples(
        st.dictionaries(keys=st.text(), values=st.text()),
        st.shared(st.text(), "key"),
    ).map(lambda x: {k: v for k, v in x[0].items() if k != x[1]}),
)
def test_it_raises_an_error_on_unknown_key(
    key: str, environ: typing.Dict[str, str]
) -> None:
    config = twelvefactor.Config(environ=environ)

    with pytest.raises(twelvefactor.ConfigError) as excinfo:
        config.get(key=key)

    assert str(excinfo.value) == "Unknown environment variable: {}".format(key)
