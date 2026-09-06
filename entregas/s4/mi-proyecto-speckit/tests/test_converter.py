"""Unit tests for temperature conversion logic."""

import math
import unittest
from src.converter import (
    AbsoluteZeroError,
    ConversionResult,
    TemperatureScale,
    convert_temperature,
)


class TestCelsiusFahrenheitConversion(unittest.TestCase):
    """Tests for User Story 1: Celsius <-> Fahrenheit conversions."""

    def test_celsius_to_fahrenheit_standard_freezing_and_boiling(self):
        """0 °C -> 32.00 °F and 100 °C -> 212.00 °F."""
        res_freezing = convert_temperature(0, "C", "F")
        self.assertEqual(res_freezing.converted_value, 32.00)
        self.assertEqual(res_freezing.formatted, "32.00 °F")
        self.assertEqual(res_freezing.from_scale, TemperatureScale.CELSIUS)
        self.assertEqual(res_freezing.to_scale, TemperatureScale.FAHRENHEIT)

        res_boiling = convert_temperature(100, "C", "F")
        self.assertEqual(res_boiling.converted_value, 212.00)
        self.assertEqual(res_boiling.formatted, "212.00 °F")

    def test_celsius_to_fahrenheit_room_temp(self):
        """25 °C -> 77.00 °F."""
        res = convert_temperature(25, TemperatureScale.CELSIUS, TemperatureScale.FAHRENHEIT)
        self.assertEqual(res.converted_value, 77.00)
        self.assertEqual(res.formatted, "77.00 °F")

    def test_fahrenheit_to_celsius_body_temp(self):
        """98.6 °F -> 37.00 °C."""
        res = convert_temperature(98.6, "F", "C")
        self.assertEqual(res.converted_value, 37.00)
        self.assertEqual(res.formatted, "37.00 °C")

    def test_fahrenheit_to_celsius_repeating_decimal_rounding(self):
        """100 °F -> 37.78 °C (tests 2 decimal places half-up rounding)."""
        res = convert_temperature(100, "F", "C")
        self.assertEqual(res.converted_value, 37.78)
        self.assertEqual(res.formatted, "37.78 °C")

    def test_coincidence_point_negative_forty(self):
        """-40 °C -> -40.00 °F and -40 °F -> -40.00 °C."""
        res_c_to_f = convert_temperature(-40, "C", "F")
        self.assertEqual(res_c_to_f.converted_value, -40.00)
        self.assertEqual(res_c_to_f.formatted, "-40.00 °F")

        res_f_to_c = convert_temperature(-40, "F", "C")
        self.assertEqual(res_f_to_c.converted_value, -40.00)
        self.assertEqual(res_f_to_c.formatted, "-40.00 °C")

    def test_identity_conversions(self):
        """Same unit conversion preserves value with 2 decimal places."""
        res_c = convert_temperature(25.5, "celsius", "c")
        self.assertEqual(res_c.converted_value, 25.50)
        self.assertEqual(res_c.formatted, "25.50 °C")

        res_f = convert_temperature(77, "fahrenheit", "f")
        self.assertEqual(res_f.converted_value, 77.00)
        self.assertEqual(res_f.formatted, "77.00 °F")


class TestKelvinConversion(unittest.TestCase):
    """Tests for User Story 2: Kelvin bidirectional and identity conversions."""

    def test_celsius_to_kelvin(self):
        """0 °C -> 273.15 K, 100 °C -> 373.15 K, -273.15 °C -> 0.00 K."""
        res_0 = convert_temperature(0, "C", "K")
        self.assertEqual(res_0.converted_value, 273.15)
        self.assertEqual(res_0.formatted, "273.15 K")

        res_100 = convert_temperature(100, "celsius", "kelvin")
        self.assertEqual(res_100.converted_value, 373.15)
        self.assertEqual(res_100.formatted, "373.15 K")

        res_abs = convert_temperature(-273.15, "C", "K")
        self.assertEqual(res_abs.converted_value, 0.00)
        self.assertEqual(res_abs.formatted, "0.00 K")

    def test_kelvin_to_celsius(self):
        """273.15 K -> 0.00 °C, 300 K -> 26.85 °C."""
        res_0 = convert_temperature(273.15, "K", "C")
        self.assertEqual(res_0.converted_value, 0.00)
        self.assertEqual(res_0.formatted, "0.00 °C")

        res_room = convert_temperature(300, "K", "C")
        self.assertEqual(res_room.converted_value, 26.85)
        self.assertEqual(res_room.formatted, "26.85 °C")

    def test_fahrenheit_to_kelvin(self):
        """32 °F -> 273.15 K, 212 °F -> 373.15 K."""
        res_freezing = convert_temperature(32, "F", "K")
        self.assertEqual(res_freezing.converted_value, 273.15)
        self.assertEqual(res_freezing.formatted, "273.15 K")

        res_boiling = convert_temperature(212, "fahrenheit", "kelvin")
        self.assertEqual(res_boiling.converted_value, 373.15)
        self.assertEqual(res_boiling.formatted, "373.15 K")

    def test_kelvin_to_fahrenheit(self):
        """373.15 K -> 212.00 °F, 273.15 K -> 32.00 °F, 0 K -> -459.67 °F."""
        res_boiling = convert_temperature(373.15, "K", "F")
        self.assertEqual(res_boiling.converted_value, 212.00)
        self.assertEqual(res_boiling.formatted, "212.00 °F")

        res_freezing = convert_temperature(273.15, "K", "F")
        self.assertEqual(res_freezing.converted_value, 32.00)
        self.assertEqual(res_freezing.formatted, "32.00 °F")

        res_zero = convert_temperature(0, "K", "F")
        self.assertEqual(res_zero.converted_value, -459.67)
        self.assertEqual(res_zero.formatted, "-459.67 °F")

    def test_kelvin_identity(self):
        """300 K -> 300.00 K."""
        res = convert_temperature(300, "kelvin", "k")
        self.assertEqual(res.converted_value, 300.00)
        self.assertEqual(res.formatted, "300.00 K")


class TestBoundaryValidation(unittest.TestCase):
    """Tests for User Story 3: Absolute zero and boundary validations."""

    def test_negative_kelvin_raises_absolute_zero_error(self):
        """Kelvin < 0 must be rejected with AbsoluteZeroError."""
        with self.assertRaises(AbsoluteZeroError) as ctx:
            convert_temperature(-0.01, "K", "C")
        self.assertIn("Kelvin temperature cannot be less than 0 K", str(ctx.exception))

        with self.assertRaises(AbsoluteZeroError) as ctx:
            convert_temperature(-5, "kelvin", "fahrenheit")
        self.assertIn("Kelvin temperature cannot be less than 0 K", str(ctx.exception))

    def test_exact_absolute_zero_accepted(self):
        """0 K, -273.15 °C, -459.67 °F are valid and accepted."""
        res_k = convert_temperature(0, "K", "C")
        self.assertEqual(res_k.converted_value, -273.15)

        res_c = convert_temperature(-273.15, "C", "K")
        self.assertEqual(res_c.converted_value, 0.0)

        res_f = convert_temperature(-459.67, "F", "K")
        self.assertEqual(res_f.converted_value, 0.0)

    def test_celsius_below_absolute_zero_rejected(self):
        """Celsius < -273.15 must be rejected."""
        with self.assertRaises(AbsoluteZeroError) as ctx:
            convert_temperature(-300, "C", "K")
        self.assertIn("below absolute zero", str(ctx.exception).lower())

    def test_fahrenheit_below_absolute_zero_rejected(self):
        """Fahrenheit < -459.67 must be rejected."""
        with self.assertRaises(AbsoluteZeroError) as ctx:
            convert_temperature(-500, "F", "C")
        self.assertIn("below absolute zero", str(ctx.exception).lower())

    def test_boolean_inputs_rejected(self):
        """Boolean inputs must be rejected with TypeError."""
        with self.assertRaises(TypeError) as ctx:
            convert_temperature(True, "C", "F")
        self.assertIn("cannot be a boolean", str(ctx.exception))

        with self.assertRaises(TypeError) as ctx:
            convert_temperature(False, "C", "F")
        self.assertIn("cannot be a boolean", str(ctx.exception))

    def test_non_finite_inputs_rejected(self):
        """NaN and Infinity values must be rejected with ValueError."""
        for val in [float("nan"), float("inf"), float("-inf"), math.nan, math.inf]:
            with self.assertRaises(ValueError) as ctx:
                convert_temperature(val, "C", "F")
            self.assertIn("must be a finite number", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
