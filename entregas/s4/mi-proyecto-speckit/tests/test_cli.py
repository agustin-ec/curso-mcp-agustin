"""Integration tests for the Command-Line Interface (CLI)."""

import io
import json
import sys
import unittest
from unittest.mock import patch
from src import cli


class TestCliCelsiusFahrenheit(unittest.TestCase):
    """Integration tests for User Story 1 CLI commands."""

    def run_cli(self, args: list[str]) -> tuple[int, str, str]:
        """Runs the CLI with given arguments capturing stdout and stderr."""
        stdout_buf = io.StringIO()
        stderr_buf = io.StringIO()
        with patch("sys.stdout", stdout_buf), patch("sys.stderr", stderr_buf):
            try:
                exit_code = cli.main(args)
            except SystemExit as exc:
                exit_code = exc.code if isinstance(exc.code, int) else 1

        return exit_code, stdout_buf.getvalue(), stderr_buf.getvalue()

    def test_cli_celsius_to_fahrenheit_text(self):
        """python3 -m src.cli 0 -f C -t F -> 32.00 °F (exit code 0)."""
        exit_code, stdout, stderr = self.run_cli(["0", "-f", "C", "-t", "F"])
        self.assertEqual(exit_code, 0)
        self.assertIn("32.00 °F", stdout.strip())

    def test_cli_fahrenheit_to_celsius_rounding_text(self):
        """python3 -m src.cli 100 -f F -t C -> 37.78 °C (exit code 0)."""
        exit_code, stdout, stderr = self.run_cli(["100", "-f", "F", "-t", "C"])
        self.assertEqual(exit_code, 0)
        self.assertIn("37.78 °C", stdout.strip())

    def test_cli_json_output_mode(self):
        """python3 -m src.cli 25 -f C -t F --json."""
        exit_code, stdout, stderr = self.run_cli(["25", "-f", "C", "-t", "F", "--json"])
        self.assertEqual(exit_code, 0)
        data = json.loads(stdout)
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["data"]["converted_value"], 77.0)
        self.assertEqual(data["data"]["formatted"], "77.00 °F")


class TestCliKelvin(unittest.TestCase):
    """Integration tests for User Story 2: Kelvin CLI commands and aliases."""

    def run_cli(self, args: list[str]) -> tuple[int, str, str]:
        stdout_buf = io.StringIO()
        stderr_buf = io.StringIO()
        with patch("sys.stdout", stdout_buf), patch("sys.stderr", stderr_buf):
            try:
                exit_code = cli.main(args)
            except SystemExit as exc:
                exit_code = exc.code if isinstance(exc.code, int) else 1
        return exit_code, stdout_buf.getvalue(), stderr_buf.getvalue()

    def test_cli_celsius_to_kelvin(self):
        """python3 -m src.cli 0 -f C -t K -> 273.15 K."""
        exit_code, stdout, stderr = self.run_cli(["0", "-f", "C", "-t", "K"])
        self.assertEqual(exit_code, 0)
        self.assertIn("273.15 K", stdout.strip())

    def test_cli_kelvin_to_fahrenheit(self):
        """python3 -m src.cli 373.15 -f K -t F -> 212.00 °F."""
        exit_code, stdout, stderr = self.run_cli(["373.15", "-f", "K", "-t", "F"])
        self.assertEqual(exit_code, 0)
        self.assertIn("212.00 °F", stdout.strip())

    def test_cli_aliases_and_case_insensitivity(self):
        """python3 -m src.cli 300 -f kelvin -t celsius -> 26.85 °C."""
        exit_code, stdout, stderr = self.run_cli(["300", "-f", "kelvin", "-t", "celsius"])
        self.assertEqual(exit_code, 0)
        self.assertIn("26.85 °C", stdout.strip())


class TestCliErrorHandling(unittest.TestCase):
    """Integration tests for User Story 3: Boundary and error handling in CLI."""

    def run_cli(self, args: list[str]) -> tuple[int, str, str]:
        stdout_buf = io.StringIO()
        stderr_buf = io.StringIO()
        with patch("sys.stdout", stdout_buf), patch("sys.stderr", stderr_buf):
            try:
                exit_code = cli.main(args)
            except SystemExit as exc:
                exit_code = exc.code if isinstance(exc.code, int) else 1
        return exit_code, stdout_buf.getvalue(), stderr_buf.getvalue()

    def test_cli_negative_kelvin_fails_with_exit_code_1(self):
        """python3 -m src.cli -5 -f K -t C -> exit code 1 with descriptive error."""
        exit_code, stdout, stderr = self.run_cli(["-5", "-f", "K", "-t", "C"])
        self.assertEqual(exit_code, 1)
        self.assertIn("Error:", stderr)
        self.assertIn("Kelvin temperature cannot be less than 0 K", stderr)

    def test_cli_negative_kelvin_json_error(self):
        """python3 -m src.cli -5 -f K -t C --json -> structured JSON error."""
        exit_code, stdout, stderr = self.run_cli(["-5", "-f", "K", "-t", "C", "--json"])
        self.assertEqual(exit_code, 1)
        err_data = json.loads(stderr)
        self.assertEqual(err_data["status"], "error")
        self.assertEqual(err_data["error"]["code"], "BELOW_ABSOLUTE_ZERO")
        self.assertIn("Kelvin temperature cannot be less than 0 K", err_data["error"]["message"])

    def test_cli_below_absolute_zero_celsius(self):
        """python3 -m src.cli -300 -f C -t K -> exit code 1."""
        exit_code, stdout, stderr = self.run_cli(["-300", "-f", "C", "-t", "K"])
        self.assertEqual(exit_code, 1)
        self.assertIn("below absolute zero", stderr.lower())

    def test_cli_invalid_scale_fails(self):
        """python3 -m src.cli 100 -f X -t C -> exit code 1."""
        exit_code, stdout, stderr = self.run_cli(["100", "-f", "X", "-t", "C"])
        self.assertEqual(exit_code, 1)
        self.assertIn("Unsupported temperature scale", stderr)


if __name__ == "__main__":
    unittest.main()
