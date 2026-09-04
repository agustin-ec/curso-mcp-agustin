# Temperature Unit Converter

Conversor de unidades de temperatura entre **Celsius (°C)**, **Fahrenheit (°F)** y **Kelvin (K)** implementado en Python 3 utilizando únicamente la biblioteca estándar.

## Características

- Conversión bidireccional entre Celsius, Fahrenheit y Kelvin.
- Redondeo estándar a 2 decimales en todos los resultados.
- Validación estricta de límites termodinámicos: rechaza cualquier temperatura en Kelvin menor a 0 ($K < 0$) y valores correspondientes por debajo del cero absoluto.
- Interfaz doble: biblioteca Python reutilizable (`src.converter`) e interfaz por línea de comandos (`python3 -m src.cli`) con salida de texto plano o JSON.

## Uso desde Línea de Comandos (CLI)

```bash
# Celsius a Fahrenheit
python3 -m src.cli 0 -f C -t F
# Salida: 32.00 °F

# Fahrenheit a Celsius (redondeo a 2 decimales)
python3 -m src.cli 100 -f F -t C
# Salida: 37.78 °C

# Kelvin a Celsius
python3 -m src.cli 273.15 -f K -t C
# Salida: 0.00 °C

# Salida estructurada JSON
python3 -m src.cli 25 -f C -t F --json
# Salida: {"status": "success", "data": {"original_value": 25.0, "from_scale": "C", "converted_value": 77.0, "to_scale": "F", "formatted": "77.00 °F"}}

# Rechazo de temperaturas bajo el cero absoluto (Kelvin < 0)
python3 -m src.cli -5 -f K -t C
# Error: Kelvin temperature cannot be less than 0 K (received: -5.0)
```

## Uso como Biblioteca Python

```python
from src.converter import convert_temperature, TemperatureScale, AbsoluteZeroError

result = convert_temperature(100, "F", "C")
print(result.converted_value)  # 37.78
print(result.formatted)        # "37.78 °C"

try:
    convert_temperature(-10, "K", "C")
except AbsoluteZeroError as e:
    print(f"Error de validación: {e}")
```

## Ejecución de Pruebas

```bash
python3 -m unittest discover -s tests -p "test_*.py" -v
```
