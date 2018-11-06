import typing
import unittest.mock as mock

import hypothesis
import hypothesis.strategies as st

import twelvefactor


@hypothesis.given(environ=st.dictionaries(keys=st.text(), values=st.text()))
def test_it_should_use_provided_environment(
    environ: typing.Dict[str, str]
) -> None:
    config = twelvefactor.Config(environ=environ)

    assert config.environ == environ


def test_it_should_uses_os_environ_by_default() -> None:
    with mock.patch("os.environ") as environ:
        config = twelvefactor.Config()

        assert config.environ == environ


def test_config() -> None:
    assert isinstance(twelvefactor.config, twelvefactor.Config)
