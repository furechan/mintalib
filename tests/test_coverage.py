"""Every core calculation must be exposed in all three stable interfaces."""

import pytest

from mintalib import core


def list_core_bases():
    return sorted(
        name.removeprefix("calc_") for name in dir(core) if name.startswith("calc_")
    )


@pytest.mark.parametrize("base", list_core_bases())
def test_function_coverage(base):
    from mintalib import functions

    assert callable(getattr(functions, base, None)), f"missing function {base!r}"


@pytest.mark.parametrize("base", list_core_bases())
def test_indicator_coverage(base):
    pytest.importorskip("pandas", reason="mintalib.indicators requires pandas")
    from mintalib import indicators

    name = base.upper()
    assert callable(getattr(indicators, name, None)), f"missing indicator {name!r}"


@pytest.mark.parametrize("base", list_core_bases())
def test_expression_coverage(base):
    pytest.importorskip("polars", reason="mintalib.expressions requires polars")
    from mintalib import expressions

    name = base.upper()
    assert callable(getattr(expressions, name, None)), f"missing expression {name!r}"
