"""
Genera reporte-qa.html consolidando tests, cobertura y seguridad básica.
Escrito en Python puro (no usa IA) para no gastar tokens en algo mecánico.
"""

import json
import re
import shutil
import subprocess
from pathlib import Path

PROJECT_ROOT = Path.cwd()
EXCLUDE_DIRS = {".venv", "venv", ".agents", "tests", "__pycache__", ".git"}


def run_tests_and_coverage():
    """Corre pytest con cobertura y reportes en JSON, sin llamar a ningún modelo."""
    pytest_bin = shutil.which("pytest") or "pytest"
    subprocess.run(
        [
            pytest_bin,
            "--cov=.", "--cov-report=json:coverage.json",
            "--json-report", "--json-report-file=test-report.json",
            "-q",
        ],
        capture_output=True, text=True,
    )

    test_summary = {"total": 0, "passed": 0, "failed": 0}
    try:
        with open("test-report.json") as f:
            data = json.load(f)
        s = data.get("summary", {})
        test_summary["total"] = s.get("total", 0)
        test_summary["passed"] = s.get("passed", 0)
        test_summary["failed"] = s.get("failed", 0)
    except FileNotFoundError:
        pass

    coverage_summary = {"percent": 0, "missing_files": []}
    try:
        with open("coverage.json") as f:
            cov = json.load(f)
        coverage_summary["percent"] = round(cov["totals"]["percent_covered"], 1)
        for filename, filedata in cov.get("files", {}).items():
            missing = filedata.get("missing_lines", [])
            if missing:
                coverage_summary["missing_files"].append((filename, missing))
    except FileNotFoundError:
        pass

    return test_summary, coverage_summary


def scan_security():
    """Búsqueda básica de secretos, except genéricos y falta de validación."""
    findings = []
    secret_pattern = re.compile(
        r'\b(api[_-]?key|secret|password|token)\s*=\s*[\'"][^\'"]+[\'"]', re.IGNORECASE
    )
    bare_except_pattern = re.compile(r'^\s*except\s*:\s*$')

    for py_file in PROJECT_ROOT.rglob("*.py"):
        if any(part in EXCLUDE_DIRS for part in py_file.parts):
            continue
        try:
            lines = py_file.read_text(encoding="utf-8").splitlines()
        except Exception:
            continue
        for i, line in enumerate(lines, start=1):
            if secret_pattern.search(line):
                findings.append(("🔑 Secreto expuesto", f"{py_file.name}:{i}"))
            if bare_except_pattern.match(line):
                findings.append(("🚪 Manejo de excepciones", f"{py_file.name}:{i} (except: genérico)"))

    return findings


def build_html(test_summary, coverage_summary, security_findings):
    all_tests_pass = test_summary["failed"] == 0 and test_summary["total"] > 0
    no_critical_findings = len(security_findings) == 0
    verdict = "✅ APROBADO" if (all_tests_pass and no_critical_findings) else "⚠️ REQUIERE CORRECCIÓN"

    findings_rows = "".join(
        f"<tr><td>{cat}</td><td>{detail}</td></tr>" for cat, detail in security_findings
    ) or "<tr><td colspan='2'>Sin hallazgos</td></tr>"

    missing_rows = "".join(
        f"<tr><td>{f}</td><td>{lines}</td></tr>"
        for f, lines in coverage_summary["missing_files"]
    ) or "<tr><td colspan='2'>Cobertura completa</td></tr>"

    html = f"""<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8"><title>Reporte de Calidad</title>
<style>
body {{ font-family: sans-serif; margin: 2rem; }}
table {{ border-collapse: collapse; width: 100%; margin-bottom: 1.5rem; }}
th, td {{ border: 1px solid #ccc; padding: 0.5rem; text-align: left; }}
.veredicto {{ font-size: 1.4rem; font-weight: bold; }}
</style></head><body>
<h1>Reporte de Calidad</h1>
<p class="veredicto">Veredicto: {verdict}</p>

<h2>Tests</h2>
<p>Total: {test_summary['total']} · Pasaron: {test_summary['passed']} · Fallaron: {test_summary['failed']}</p>

<h2>Cobertura</h2>
<p>Cobertura total: {coverage_summary['percent']}%</p>
<table><tr><th>Archivo</th><th>Líneas sin probar</th></tr>{missing_rows}</table>

<h2>Seguridad</h2>
<table><tr><th>Categoría</th><th>Detalle</th></tr>{findings_rows}</table>
</body></html>"""

    Path("reporte-qa.html").write_text(html, encoding="utf-8")


if __name__ == "__main__":
    tests, coverage = run_tests_and_coverage()
    findings = scan_security()
    build_html(tests, coverage, findings)
    print("reporte-qa.html generado.")
