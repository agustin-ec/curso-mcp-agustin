"""Convertidor de unidades de temperatura (Celsius, Fahrenheit, Kelvin).

Implementación según la especificación definida en spec_manual.md.
"""

from __future__ import annotations

from enum import Enum
import math
import sys
from typing import Any


class InvalidTemperatureError(ValueError, TypeError):
    """Excepción para errores de valor o tipo en conversiones de temperatura.

    Hereda tanto de ValueError como de TypeError para permitir que el código cliente
    capture el error esperado con cualquiera de las dos excepciones estándar.
    """
    pass


class Unit(str, Enum):
    """Unidades de temperatura soportadas."""
    CELSIUS = "C"
    FAHRENHEIT = "F"
    KELVIN = "K"


# Mapeo de alias y nombres permitidos para cada unidad
_UNIT_ALIASES: dict[str, Unit] = {
    "c": Unit.CELSIUS,
    "celsius": Unit.CELSIUS,
    "centigrados": Unit.CELSIUS,
    "centigrado": Unit.CELSIUS,
    "f": Unit.FAHRENHEIT,
    "fahrenheit": Unit.FAHRENHEIT,
    "k": Unit.KELVIN,
    "kelvin": Unit.KELVIN,
}


def normalize_unit(unit: str | Unit) -> Unit:
    """Normaliza y valida la unidad de temperatura especificada."""
    if isinstance(unit, Unit):
        return unit
    if not isinstance(unit, str):
        raise InvalidTemperatureError(
            f"La unidad de temperatura debe ser una cadena o Unit enum. Se recibió: {unit!r}"
        )

    clean = unit.strip().lower().replace("°", "")
    if clean in _UNIT_ALIASES:
        return _UNIT_ALIASES[clean]

    raise InvalidTemperatureError(
        f"Unidad no válida: {unit!r}. Las unidades soportadas son Celsius (C), Fahrenheit (F) y Kelvin (K)."
    )


def validate_temperature_value(value: Any) -> float:
    """Valida y convierte el valor de entrada a un número float."""
    if value is None:
        raise InvalidTemperatureError(
            "El valor de temperatura debe ser numérico y no puede ser None."
        )

    if isinstance(value, bool):
        raise InvalidTemperatureError(
            f"El valor de temperatura debe ser numérico. Se recibió un booleano: {value!r}"
        )

    if isinstance(value, str) and not value.strip():
        raise InvalidTemperatureError(
            f"El valor de temperatura debe ser numérico. Se recibió una cadena vacía: {value!r}"
        )

    try:
        val = float(value)
    except (ValueError, TypeError):
        raise InvalidTemperatureError(
            f"Valor no numérico como entrada: {value!r}. Debe ser un número int o float válido."
        )

    if math.isnan(val) or math.isinf(val):
        raise InvalidTemperatureError(
            f"El valor de temperatura debe ser numérico y finito. Se recibió: {val}"
        )

    return val


def convertir_temperatura(
    valor: Any = None,
    origen: str | Unit | None = None,
    destino: str | Unit | None = None,
    *,
    value: Any = None,
    desde: str | Unit | None = None,
    hacia: str | Unit | None = None,
    from_unit: str | Unit | None = None,
    to_unit: str | Unit | None = None,
) -> float:
    """Convierte una temperatura entre Celsius, Fahrenheit y Kelvin.

    Args:
        valor: Valor numérico a convertir (int, float o string numérico).
        origen: Unidad de origen ('C', 'F', 'K' o nombres completos como 'Celsius').
        destino: Unidad de destino ('C', 'F', 'K' o nombres completos).
        value: Alias para 'valor'.
        desde: Alias para 'origen'.
        hacia: Alias para 'destino'.
        from_unit: Alias en inglés para 'origen'.
        to_unit: Alias en inglés para 'destino'.

    Returns:
        Temperatura convertida redondeada a 2 decimales.

    Raises:
        InvalidTemperatureError (ValueError, TypeError):
            - Si el valor no es numérico (ej. "abc").
            - Si la temperatura en Kelvin es menor a 0.
            - Si las unidades no son válidas.
    """
    # Resolver alias para valor
    val_raw = valor if valor is not None else value
    if val_raw is None:
        raise InvalidTemperatureError("El valor de temperatura debe ser numérico y no puede ser None.")

    # Resolver alias para origen y destino
    orig_raw = origen or desde or from_unit
    dest_raw = destino or hacia or to_unit

    if orig_raw is None or dest_raw is None:
        raise InvalidTemperatureError("Debe especificarse la unidad de origen y destino.")

    # Validar valor numérico
    val = validate_temperature_value(val_raw)

    # Validar unidades
    unit_orig = normalize_unit(orig_raw)
    unit_dest = normalize_unit(dest_raw)

    # Criterio: Rechaza una temperatura en Kelvin menor a 0
    if unit_orig == Unit.KELVIN and val < 0:
        raise InvalidTemperatureError(
            f"Temperatura en Kelvin inválida: no puede ser menor a 0 (cero absoluto). Se recibió: {val}"
        )

    # Caso borde: Mismo valor de entrada y salida
    if unit_orig == unit_dest:
        return round(val, 2)

    # Conversión a Celsius como escala base intermedia
    if unit_orig == Unit.CELSIUS:
        celsius = val
    elif unit_orig == Unit.FAHRENHEIT:
        celsius = (val - 32.0) * 5.0 / 9.0
    elif unit_orig == Unit.KELVIN:
        celsius = val - 273.15
    else:
        raise InvalidTemperatureError(f"Unidad de origen no soportada: {unit_orig}")

    # Conversión desde Celsius a la unidad destino
    if unit_dest == Unit.CELSIUS:
        res = celsius
    elif unit_dest == Unit.FAHRENHEIT:
        res = celsius * 9.0 / 5.0 + 32.0
    elif unit_dest == Unit.KELVIN:
        res = celsius + 273.15
        if round(res, 2) < 0:
            raise InvalidTemperatureError(
                f"Temperatura en Kelvin inválida: la temperatura resultante no puede ser menor a 0. Se calculó: {round(res, 2)}"
            )
    else:
        raise InvalidTemperatureError(f"Unidad de destino no soportada: {unit_dest}")

    # Criterio: Redondea el resultado a 2 decimales
    return round(res, 2)


# Alias en inglés para compatibilidad
convert_temperature = convertir_temperatura


# Funciones específicas de conveniencia
def celsius_a_fahrenheit(c: Any) -> float:
    """Convierte Celsius a Fahrenheit redondeado a 2 decimales."""
    return convertir_temperatura(c, Unit.CELSIUS, Unit.FAHRENHEIT)


def fahrenheit_a_celsius(f: Any) -> float:
    """Convierte Fahrenheit a Celsius redondeado a 2 decimales."""
    return convertir_temperatura(f, Unit.FAHRENHEIT, Unit.CELSIUS)


def celsius_a_kelvin(c: Any) -> float:
    """Convierte Celsius a Kelvin redondeado a 2 decimales."""
    return convertir_temperatura(c, Unit.CELSIUS, Unit.KELVIN)


def kelvin_a_celsius(k: Any) -> float:
    """Convierte Kelvin a Celsius redondeado a 2 decimales."""
    return convertir_temperatura(k, Unit.KELVIN, Unit.CELSIUS)


def fahrenheit_a_kelvin(f: Any) -> float:
    """Convierte Fahrenheit a Kelvin redondeado a 2 decimales."""
    return convertir_temperatura(f, Unit.FAHRENHEIT, Unit.KELVIN)


def kelvin_a_fahrenheit(k: Any) -> float:
    """Convierte Kelvin a Fahrenheit redondeado a 2 decimales."""
    return convertir_temperatura(k, Unit.KELVIN, Unit.FAHRENHEIT)


# Alias en inglés de las funciones específicas
celsius_to_fahrenheit = celsius_a_fahrenheit
fahrenheit_to_celsius = fahrenheit_a_celsius
celsius_to_kelvin = celsius_a_kelvin
kelvin_to_celsius = kelvin_a_celsius
fahrenheit_to_kelvin = fahrenheit_a_kelvin
kelvin_to_fahrenheit = kelvin_a_fahrenheit


def main() -> None:
    """Interfaz de línea de comandos para el convertidor de temperatura."""
    args = sys.argv[1:]
    if len(args) != 3:
        print("Uso: python converter.py <valor> <unidad_origen> <unidad_destino>")
        print("Ejemplos:")
        print("  python converter.py 100 C F")
        print("  python converter.py 0 C K")
        print("  python converter.py 98.6 F C")
        sys.exit(1)

    valor_arg, origen_arg, destino_arg = args
    try:
        resultado = convertir_temperatura(valor_arg, origen_arg, destino_arg)
        print(f"{valor_arg} °{origen_arg.upper()} = {resultado} °{destino_arg.upper()}")
    except InvalidTemperatureError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
