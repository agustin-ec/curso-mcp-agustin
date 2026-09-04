"""Command-line interface entrypoint for Temperature Unit Converter."""

from __future__ import annotations

import argparse
import json
import sys
from typing import List, Optional

from src.converter import (
    AbsoluteZeroError,
    ConversionResult,
    InvalidScaleError,
    TemperatureError,
    convert_temperature,
)


def create_parser() -> argparse.ArgumentParser:
    """Builds the argument parser for temperature conversion."""
    parser = argparse.ArgumentParser(
        prog="temperature-converter",
        description="Convert temperature values between Celsius, Fahrenheit, and Kelvin.",
    )
    parser.add_argument(
        "value",
        type=float,
        help="Numeric temperature value to convert (e.g. 100, 37.5, -40).",
    )
    parser.add_argument(
        "-f",
        "--from",
        dest="from_scale",
        required=True,
        help="Source temperature scale (C, F, K).",
    )
    parser.add_argument(
        "-t",
        "--to",
        dest="to_scale",
        required=True,
        help="Target temperature scale (C, F, K).",
    )
    parser.add_argument(
        "-j",
        "--json",
        action="store_true",
        help="Output structured JSON response instead of plain text.",
    )
    return parser


def format_success_json(result: ConversionResult) -> str:
    """Formats a successful result as a JSON string."""
    return json.dumps(
        {
            "status": "success",
            "data": {
                "original_value": result.original_value,
                "from_scale": result.from_scale.value,
                "converted_value": result.converted_value,
                "to_scale": result.to_scale.value,
                "formatted": result.formatted,
            },
        },
        indent=2 if sys.stdout.isatty() else None,
    )


def format_error_json(code: str, message: str) -> str:
    """Formats an error response as a JSON string."""
    return json.dumps(
        {
            "status": "error",
            "error": {
                "code": code,
                "message": message,
            },
        }
    )


def main(argv: Optional[List[str]] = None) -> int:
    """Main CLI execution handler."""
    parser = create_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return exc.code if isinstance(exc.code, int) else 2

    try:
        result = convert_temperature(
            value=args.value,
            from_scale=args.from_scale,
            to_scale=args.to_scale,
        )
        if args.json:
            print(format_success_json(result))
        else:
            print(result.formatted)
        return 0

    except AbsoluteZeroError as exc:
        if args.json:
            print(format_error_json("BELOW_ABSOLUTE_ZERO", str(exc)), file=sys.stderr)
        else:
            print(f"Error: {exc}", file=sys.stderr)
        return 1

    except (InvalidScaleError, TemperatureError, ValueError, TypeError) as exc:
        if args.json:
            print(format_error_json("INVALID_INPUT", str(exc)), file=sys.stderr)
        else:
            print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
