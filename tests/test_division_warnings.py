import warnings

import numpy as np
import pytest

from mintalib import core


@pytest.mark.parametrize("backend", ["core", "polars"])
@pytest.mark.parametrize("name,price,spread,zero_from", [
    pytest.param("cci", 10.0, 0.0, (None,), id="cci-flat"),
    pytest.param("stoch", 10.0, 0.0, (None, None), id="stoch-flat"),
    pytest.param("ppo", 0.0, 0.0, (None, None, None), id="ppo-zero"),
    pytest.param("dmi", 10.0, 0.0, (None, None, None), id="dmi-flat"),
    pytest.param("adx", 10.0, 0.0, (None,), id="adx-flat"),
    pytest.param("pdi", 10.0, 0.0, (None,), id="pdi-flat"),
    pytest.param("mdi", 10.0, 0.0, (None,), id="mdi-flat"),
    pytest.param("macdv", 10.0, 0.0, (None, None, None), id="macdv-flat"),
    pytest.param("dmi", 10.0, 1.0, (None, 13, 13), id="dmi-no-movement"),
    pytest.param("adx", 10.0, 1.0, (None,), id="adx-no-movement"),
])
def test_zero_denominator_outputs_without_warnings(backend, name, price, spread, zero_from):
    size = 100
    close = np.full(size, price)
    data = {"high": close + spread, "low": close - spread, "close": close}
    expected = []
    for start in zero_from:
        values = np.full(size, np.nan)
        if start is not None:
            # Default DI period is 14; initialized directional indexes are zero.
            values[start:] = 0.0
        expected.append(values)

    if backend == "core":
        calc = getattr(core, f"calc_{name}")
        inputs = getattr(calc, "metadata", {}).get("inputs", ("close",))
        with warnings.catch_warnings():
            warnings.simplefilter("error", RuntimeWarning)
            result = calc(*(data[key] for key in inputs))
        outputs = result if isinstance(result, tuple) else (result,)
        assert len(outputs) == len(expected)
        for output, values in zip(outputs, expected):
            np.testing.assert_array_equal(output, values)
    else:
        pl = pytest.importorskip("polars")
        from mintalib import expressions

        frame = pl.DataFrame(data)
        expr = getattr(expressions, name.upper())()
        with warnings.catch_warnings():
            warnings.simplefilter("error", RuntimeWarning)
            result = frame.select(expr)
        if len(expected) > 1:
            result = result.unnest(name)
        assert result.shape == (size, len(expected))
        for output, values in zip(result.iter_columns(), expected):
            assert output.dtype == pl.Float64
            assert output.to_list() == [None if np.isnan(value) else value for value in values]
