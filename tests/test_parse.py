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


@hypothesis.given(value=st.sampled_from(TRUE_STRINGS))
def test_it_should_be_able_to_parse_true(value: str) -> None:
    """
    it should be able to parse true.
    """

    config = twelvefactor.Config()

    assert config.parse(value=value, type_=bool)


@hypothesis.given(value=st.text().filter(lambda x: x not in TRUE_STRINGS))
def test_it_should_be_able_to_parse_false(value: str) -> None:
    """
    it should be able to parse false.
    """
    config = twelvefactor.Config()

    assert not config.parse(value=value, type_=bool)


@hypothesis.given(value=st.text())
def test_it_should_be_able_to_parse_strings(value: str) -> None:
    """
    it should be able to parse strings.
    """
    config = twelvefactor.Config()

    assert config.parse(value=value) == value


@hypothesis.given(value=st.integers())
def test_it_should_be_able_to_parse_integers(value: int) -> None:
    """
    it should be able to parse integers.
    """
    config = twelvefactor.Config()

    assert config.parse(value=str(value), type_=int) == value


@hypothesis.given(value=st.floats())
def test_it_should_be_able_to_parse_floats(value: float) -> None:
    """
    it should be able to parse floats.
    """
    config = twelvefactor.Config()

    result = config.parse(value=str(value), type_=float)

    if math.isnan(value):
        assert math.isnan(result)
    else:
        assert result == value


@hypothesis.given(value=st.complex_numbers())
def test_it_should_be_able_to_parse_complex_numbers(value: complex) -> None:
    config = twelvefactor.Config()

    result = config.parse(value=str(value), type_=complex)

    if cmath.isnan(value):
        assert cmath.isnan(result)
    else:
        assert result == value


@hypothesis.given(value=st.lists(elements=st.booleans()))
def test_it_should_be_able_to_parse_boolean_list(
    value: typing.List[bool]
) -> None:
    config = twelvefactor.Config()

    result = config.parse(
        value=",".join(str(v) for v in value), type_=list, subtype=bool
    )

    assert result == value


@hypothesis.given(value=st.lists(elements=st.booleans()).map(tuple))
def test_it_should_be_able_to_parse_boolean_tuple(
    value: typing.Tuple[bool, ...]
) -> None:
    config = twelvefactor.Config()

    result = config.parse(
        value=",".join(str(v) for v in value), type_=tuple, subtype=bool
    )

    assert result == value


@hypothesis.given(value=st.lists(elements=st.booleans()).map(set))
def test_it_should_be_able_to_parse_boolean_set(
    value: typing.Set[bool]
) -> None:
    config = twelvefactor.Config()

    result = config.parse(
        value=",".join(str(v) for v in value), type_=set, subtype=bool
    )

    assert result == value


@hypothesis.given(value=st.lists(elements=st.booleans()).map(frozenset))
def test_it_should_be_able_to_parse_boolean_frozenset(
    value: typing.FrozenSet[bool]
) -> None:
    config = twelvefactor.Config()

    result = config.parse(
        value=",".join(str(v) for v in value), type_=frozenset, subtype=bool
    )

    assert result == value


@hypothesis.given(value=st.lists(elements=st.integers()))
def test_it_should_be_able_to_parse_integer_list(
    value: typing.List[int]
) -> None:
    config = twelvefactor.Config()

    result = config.parse(
        value=",".join(str(v) for v in value), type_=list, subtype=int
    )

    assert result == value


@hypothesis.given(value=st.lists(elements=st.integers()).map(tuple))
def test_it_should_be_able_to_parse_integer_tuple(
    value: typing.Tuple[int, ...]
) -> None:
    config = twelvefactor.Config()

    result = config.parse(
        value=",".join(str(v) for v in value), type_=tuple, subtype=int
    )

    assert result == value


@hypothesis.given(value=st.lists(elements=st.integers()).map(set))
def test_it_should_be_able_to_parse_integer_set(
    value: typing.Set[int]
) -> None:
    config = twelvefactor.Config()

    result = config.parse(
        value=",".join(str(v) for v in value), type_=set, subtype=int
    )

    assert result == value


@hypothesis.given(value=st.lists(elements=st.integers()).map(frozenset))
def test_it_should_be_able_to_parse_integer_frozenset(
    value: typing.FrozenSet[int]
) -> None:
    config = twelvefactor.Config()

    result = config.parse(
        value=",".join(str(v) for v in value), type_=frozenset, subtype=int
    )

    assert result == value


@hypothesis.given(value=st.lists(elements=st.floats(allow_nan=False)))
def test_it_should_be_able_to_parse_float_list(
    value: typing.List[float]
) -> None:
    config = twelvefactor.Config()

    result = config.parse(
        value=",".join(str(v) for v in value), type_=list, subtype=float
    )

    assert result == value


@hypothesis.given(
    value=st.lists(elements=st.floats(allow_nan=False)).map(tuple)
)
def test_it_should_be_able_to_parse_float_tuple(
    value: typing.Tuple[float, ...]
) -> None:
    config = twelvefactor.Config()

    result = config.parse(
        value=",".join(str(v) for v in value), type_=tuple, subtype=float
    )

    assert result == value


@hypothesis.given(value=st.lists(elements=st.floats(allow_nan=False)).map(set))
def test_it_should_be_able_to_parse_float_set(
    value: typing.Set[float]
) -> None:
    config = twelvefactor.Config()

    result = config.parse(
        value=",".join(str(v) for v in value), type_=set, subtype=float
    )

    assert result == value


@hypothesis.given(
    value=st.lists(elements=st.floats(allow_nan=False)).map(frozenset)
)
def test_it_should_be_able_to_parse_float_frozenset(
    value: typing.FrozenSet[float]
) -> None:
    config = twelvefactor.Config()

    result = config.parse(
        value=",".join(str(v) for v in value), type_=frozenset, subtype=float
    )

    assert result == value


@hypothesis.given(value=st.lists(elements=st.complex_numbers(allow_nan=False)))
def test_it_should_be_able_to_parse_complex_number_list(
    value: typing.List[complex]
) -> None:
    config = twelvefactor.Config()

    result = config.parse(
        value=",".join(str(v) for v in value), type_=list, subtype=complex
    )

    assert result == value


@hypothesis.given(
    value=st.lists(elements=st.complex_numbers(allow_nan=False)).map(tuple)
)
def test_it_should_be_able_to_parse_complex_number_tuple(
    value: typing.Tuple[complex, ...]
) -> None:
    config = twelvefactor.Config()

    result = config.parse(
        value=",".join(str(v) for v in value), type_=tuple, subtype=complex
    )

    assert result == value


@hypothesis.given(
    value=st.lists(elements=st.complex_numbers(allow_nan=False)).map(set)
)
def test_it_should_be_able_to_parse_complex_number_set(
    value: typing.Set[complex]
) -> None:
    config = twelvefactor.Config()

    result = config.parse(
        value=",".join(str(v) for v in value), type_=set, subtype=complex
    )

    assert result == value


@hypothesis.given(
    value=st.lists(elements=st.complex_numbers(allow_nan=False)).map(frozenset)
)
def test_it_should_be_able_to_parse_complex_number_frozenset(
    value: typing.FrozenSet[complex]
) -> None:
    config = twelvefactor.Config()

    result = config.parse(
        value=",".join(str(v) for v in value), type_=frozenset, subtype=complex
    )

    assert result == value


@hypothesis.given(
    value=st.lists(
        elements=st.text().filter(
            lambda x: "," not in x and x.strip(" ") == x and bool(x.strip(" "))
        )
    )
)
def test_it_should_be_able_to_parse_string_list(
    value: typing.List[str]
) -> None:
    config = twelvefactor.Config()

    result = config.parse(value=",".join(value), type_=list)

    assert result == value


@hypothesis.given(
    value=st.lists(
        elements=st.text().filter(
            lambda x: "," not in x and x.strip(" ") == x and bool(x.strip(" "))
        )
    ).map(tuple)
)
def test_it_should_be_able_to_parse_string_tuple(
    value: typing.Tuple[str, ...]
) -> None:
    config = twelvefactor.Config()

    result = config.parse(value=",".join(value), type_=tuple)

    assert result == value


@hypothesis.given(
    value=st.lists(
        elements=st.text().filter(
            lambda x: "," not in x and x.strip(" ") == x and bool(x.strip(" "))
        )
    ).map(set)
)
def test_it_should_be_able_to_parse_string_set(value: typing.Set[str]) -> None:
    config = twelvefactor.Config()

    result = config.parse(value=",".join(value), type_=set)

    assert result == value


@hypothesis.given(
    value=st.lists(
        elements=st.text().filter(
            lambda x: "," not in x and x.strip(" ") == x and bool(x.strip(" "))
        )
    ).map(frozenset)
)
def test_it_should_be_able_to_parse_string_frozenset(
    value: typing.FrozenSet[str]
) -> None:
    config = twelvefactor.Config()

    result = config.parse(value=",".join(value), type_=frozenset)

    assert result == value


@hypothesis.given(
    value=st.lists(
        elements=st.text().filter(
            lambda x: "," not in x and x.strip(" ") == x and bool(x.strip(" "))
        )
    )
)
def test_it_should_be_able_to_parse_string_list_with_extra_space(
    value: typing.List[str]
) -> None:
    config = twelvefactor.Config()

    result = config.parse(value="   ,   ".join(value), type_=list)

    assert result == value


@hypothesis.given(value=st.text(), error=st.text())
def test_it_should_raise_error_on_invalid_value(
    value: str, error: str
) -> None:
    config = twelvefactor.Config()

    type_ = mock.Mock(side_effect=ValueError(error))

    with pytest.raises(twelvefactor.ConfigError) as excinfo:
        config.parse(value=value, type_=type_)

    assert str(excinfo.value) == error
