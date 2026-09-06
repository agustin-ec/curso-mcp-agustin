"""Unit tests generated according to test-spec.md."""

import pytest
from src.converter import (
    AbsoluteZeroError,
    convert_temperature,
)


def test_convert_celsius_to_fahrenheit():
    """convert_temperature: dado 25°C a Fahrenheit, debe devolver 77°F."""
    res = convert_temperature(25, "C", "F")
    assert res.converted_value == 77.0
    assert res.formatted == "77.00 °F"


def test_convert_temperature_invalid_text():
    """convert_temperature: con texto en vez de número, debe dar error claro, no una excepción sin control."""
    with pytest.raises(TypeError) as excinfo:
        convert_temperature("texto", "C", "F")
    assert "Temperature value must be a valid number" in str(excinfo.value)


def test_convert_temperature_negative_kelvin():
    """convert_temperature: con Kelvin negativo, debe rechazarlo."""
    with pytest.raises(AbsoluteZeroError) as excinfo:
        convert_temperature(-1, "K", "C")
    assert "Kelvin temperature cannot be less than 0 K" in str(excinfo.value)
