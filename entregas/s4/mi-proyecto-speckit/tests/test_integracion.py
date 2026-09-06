"""Integration test generated according to test-spec.md."""

from src import cli


def test_full_conversion_flow_end_to_end(capsys):
    """Flujo completo: pedir conversión -> validar entrada -> devolver resultado de punta a punta."""
    exit_code = cli.main(["25", "-f", "C", "-t", "F"])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert "77.00 °F" in captured.out
    assert captured.err == ""
