from functools import partial
import pytest
from blk.types import Float

approx = partial(pytest.approx, rel=1e-05, abs=1e-08)


@pytest.mark.parametrize(['sample', 'expected'], [
    pytest.param(123.456, 123.456, id='usual'),
    pytest.param(3.4028235e+38, 3.4028235e+38, id='max'),
    pytest.param(-3.4028235e+38, -3.4028235e+38, id='min'),
    pytest.param(1.1754944e-38, 1.1754944e-38, id='tiny'),
])
def test_of(sample, expected):
    assert Float.of(sample) == approx(expected)


@pytest.mark.parametrize('sample', [
    pytest.param('1.0', id='str'),
])
def test_of_non_number_raises_type_error(sample):
    with pytest.raises(TypeError) as ei:
        Float.of(sample)
    print(ei.value)


@pytest.mark.parametrize('sample', [
    pytest.param(3.4028236e+38, id='over max'),
    pytest.param(-3.4028236e+38, id='under min'),
])
def test_out_of_range_raises_value_error(sample):
    with pytest.raises(ValueError) as ei:
        Float.of(sample)
    print(ei.value)


@pytest.mark.parametrize(['x', 'y'], [
    pytest.param(Float(0.0), 1e-8, id='abs'),
    pytest.param(Float(1.0), 1 + 1e-5, id='rel'),
    pytest.param(Float(1234.5678), 1234.568, id='usual'),
])
def test_eq(x, y):
    assert x == y


@pytest.mark.parametrize(['value', 'text'], [
    pytest.param(Float(1234.5678), 'Float(1234.568)', id='usual')
])
def test_repr(value, text):
    assert repr(value) == text
    assert eval(text) == value

