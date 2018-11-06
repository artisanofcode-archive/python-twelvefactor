import typing
import unittest.mock as mock

import hypothesis
import hypothesis.strategies as st

import twelvefactor

SIMPLE_OBJECTS: typing.List[st.SearchStrategy[typing.Any]] = [
    st.booleans(),
    st.text(),
    st.integers(),
    st.floats(allow_nan=False),
    st.complex_numbers(allow_nan=False),
]

COMPLEX_OBJECTS: typing.List[
    st.SearchStrategy[typing.Any]
] = SIMPLE_OBJECTS + [
    st.lists(
        elements=simple.filter(
            lambda x: (
                "," not in str(x)
                and str(x).strip(" ") == str(x)
                and bool(str(x).strip(" "))
            )
        )
    ).map(lambda x: iterable(x))
    for simple in SIMPLE_OBJECTS
    for iterable in (frozenset, set, list, tuple)
]


SIMPLE_SCHEMA = st.lists(
    elements=st.tuples(
        # KEY
        st.text(),
        # VALUE
        st.one_of(SIMPLE_OBJECTS),
    ),
    unique_by=lambda x: x[0],
)

REGULAR_SCHEMA = st.lists(
    elements=st.tuples(
        # KEY
        st.text(),
        # VALUE
        st.one_of(COMPLEX_OBJECTS),
        # DEFAULT
        st.booleans(),
        # KEY IN ENVIRON
        st.one_of(st.text(), st.none()),
    ),
    unique_by=lambda x: x[0],
)


@hypothesis.given(
    schema=st.shared(SIMPLE_SCHEMA, key="data").map(
        lambda x: {k: type(v) for k, v in x}
    ),
    environ=st.shared(SIMPLE_SCHEMA, key="data").map(
        lambda x: {k: str(v) for k, v in x}
    ),
    expected=st.shared(SIMPLE_SCHEMA, key="data").map(
        lambda x: {k: v for k, v in x}
    ),
)
def test_it_can_handle_simple_schemas(
    schema: twelvefactor.Schema,
    environ: typing.Dict[str, str],
    expected: typing.Dict[str, object],
) -> None:
    config = twelvefactor.Config(environ=environ)

    assert config(schema) == expected


@hypothesis.given(
    schema=st.shared(REGULAR_SCHEMA, key="data").map(
        lambda x: {
            k: dict(
                {"subtype": type(list(v)[0])}
                if isinstance(v, (frozenset, set, tuple, list)) and v
                else {},
                **dict(
                    {"default": v} if d else {},
                    type=type(v),
                    **({"key": k2} if k2 is not None else {})
                )
            )
            for k, v, d, k2 in x
        }
    ),
    environ=st.shared(REGULAR_SCHEMA, key="data").map(
        lambda x: {
            k2
            if k2 is not None
            else k: ",".join(str(x) for x in v)
            if isinstance(v, (frozenset, set, tuple, list))
            else str(v)
            for k, v, d, k2 in x
            if not d
        }
    ),
    expected=st.shared(REGULAR_SCHEMA, key="data").map(
        lambda x: {k: v for k, v, _, _ in x}
    ),
)
def test_it_can_handle_moderatly_complex_schemas(
    schema: twelvefactor.Schema,
    environ: typing.Dict[str, str],
    expected: typing.Dict[str, object],
) -> None:
    # guard against duplicate environ keys
    hypothesis.assume(
        len({v.get("key", k) for k, v in schema.items()}) == len(schema)
    )

    config = twelvefactor.Config(environ=environ)

    assert config(schema) == expected


@hypothesis.given(
    schema=st.shared(
        st.lists(
            elements=st.tuples(
                # KEY
                st.text(),
                # VALUE
                st.one_of(SIMPLE_OBJECTS),
            ),
            min_size=1,
            max_size=1,
        ),
        key="data",
    ).map(
        lambda x: {
            k: {"type": type(v), "mapper": mock.Mock(return_value=v)}
            for k, v in x
        }
    ),
    environ=st.shared(
        st.lists(
            elements=st.tuples(
                # KEY
                st.text(),
                # VALUE
                st.one_of(SIMPLE_OBJECTS),
            ),
            min_size=1,
            max_size=1,
        ),
        key="data",
    ).map(lambda x: {k: str(v) for k, v in x}),
    value=st.shared(
        st.lists(
            elements=st.tuples(
                # KEY
                st.text(),
                # VALUE
                st.one_of(SIMPLE_OBJECTS),
            ),
            min_size=1,
            max_size=1,
        ),
        key="data",
    ).map(lambda x: x[0][1]),
)
def test_it_should_apply_mapper(
    schema: twelvefactor.Schema,
    environ: typing.Dict[str, str],
    value: typing.Any,
) -> None:
    config = twelvefactor.Config(environ=environ)

    key = list(schema.keys())[0]

    mapper = typing.cast(mock.Mock, schema[key]["mapper"])

    assert config(schema) == {key: mapper.return_value}

    mapper.assert_called_once_with(value)
