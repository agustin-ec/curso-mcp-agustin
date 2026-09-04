"""Pruebas unitarias para el convertidor de temperatura.

Verifica todos los criterios de aceptación y casos borde descritos en spec_manual.md:
- Conversión correcta Celsius <-> Fahrenheit
- Conversión correcta Celsius <-> Kelvin
- Conversión Fahrenheit <-> Kelvin
- Redondeo a 2 decimales
- Rechazo de temperaturas en Kelvin menores a 0
- Casos borde: valor no numérico ("abc"), mismo origen/destino, negativos válidos.
"""

import unittest

from converter import (
    InvalidTemperatureError,
    Unit,
    celsius_a_fahrenheit,
    celsius_a_kelvin,
    celsius_to_fahrenheit,
    celsius_to_kelvin,
    convert_temperature,
    convertir_temperatura,
    fahrenheit_a_celsius,
    fahrenheit_a_kelvin,
    fahrenheit_to_celsius,
    fahrenheit_to_kelvin,
    kelvin_a_celsius,
    kelvin_a_fahrenheit,
    kelvin_to_celsius,
    kelvin_to_fahrenheit,
)


class TestConversorTemperatura(unittest.TestCase):
    # =========================================================================
    # Criterio 1: Convierte correctamente de Celsius a Fahrenheit y viceversa
    # =========================================================================
    def test_celsius_a_fahrenheit(self):
        self.assertEqual(convertir_temperatura(0, "C", "F"), 32.0)
        self.assertEqual(convertir_temperatura(100, "C", "F"), 212.0)
        self.assertEqual(convertir_temperatura(37, "C", "F"), 98.6)
        self.assertEqual(convertir_temperatura(20, "Celsius", "Fahrenheit"), 68.0)

    def test_fahrenheit_a_celsius(self):
        self.assertEqual(convertir_temperatura(32, "F", "C"), 0.0)
        self.assertEqual(convertir_temperatura(212, "F", "C"), 100.0)
        self.assertEqual(convertir_temperatura(98.6, "F", "C"), 37.0)
        self.assertEqual(convertir_temperatura(68, "Fahrenheit", "Celsius"), 20.0)

    # =========================================================================
    # Criterio 2: Convierte correctamente de Celsius a Kelvin y viceversa
    # =========================================================================
    def test_celsius_a_kelvin(self):
        self.assertEqual(convertir_temperatura(0, "C", "K"), 273.15)
        self.assertEqual(convertir_temperatura(100, "C", "K"), 373.15)
        self.assertEqual(convertir_temperatura(-273.15, "C", "K"), 0.0)
        self.assertEqual(convertir_temperatura(25, "Celsius", "Kelvin"), 298.15)

    def test_kelvin_a_celsius(self):
        self.assertEqual(convertir_temperatura(273.15, "K", "C"), 0.0)
        self.assertEqual(convertir_temperatura(373.15, "K", "C"), 100.0)
        self.assertEqual(convertir_temperatura(0, "K", "C"), -273.15)
        self.assertEqual(convertir_temperatura(298.15, "Kelvin", "Celsius"), 25.0)

    # =========================================================================
    # Conversión complementaria: Fahrenheit <-> Kelvin
    # =========================================================================
    def test_fahrenheit_a_kelvin(self):
        self.assertEqual(convertir_temperatura(32, "F", "K"), 273.15)
        self.assertEqual(convertir_temperatura(212, "F", "K"), 373.15)
        self.assertEqual(convertir_temperatura(-459.67, "F", "K"), 0.0)

    def test_kelvin_a_fahrenheit(self):
        self.assertEqual(convertir_temperatura(273.15, "K", "F"), 32.0)
        self.assertEqual(convertir_temperatura(373.15, "K", "F"), 212.0)
        self.assertEqual(convertir_temperatura(0, "K", "F"), -459.67)

    # =========================================================================
    # Criterio 3: Redondea el resultado a 2 decimales
    # =========================================================================
    def test_redondeo_a_dos_decimales(self):
        # 15 °F -> (15 - 32) * 5/9 = -9.4444... -> -9.44 °C
        self.assertEqual(convertir_temperatura(15, "F", "C"), -9.44)
        # 33.333 °C a °F: 33.333 * 1.8 + 32 = 91.9994 -> 92.0
        self.assertEqual(convertir_temperatura(33.333, "C", "F"), 92.0)
        # 1 °C a K: 1 + 273.15 = 274.15
        self.assertEqual(convertir_temperatura(1, "C", "K"), 274.15)
        # 75.555 °F a °C: (75.555 - 32) * 5/9 = 24.1972... -> 24.2
        self.assertEqual(convertir_temperatura(75.555, "F", "C"), 24.2)

    # =========================================================================
    # Criterio 4: Rechaza una temperatura en Kelvin menor a 0
    # =========================================================================
    def test_rechaza_kelvin_menor_a_cero(self):
        # Rechaza Kelvin negativo de entrada
        with self.assertRaises((ValueError, InvalidTemperatureError)):
            convertir_temperatura(-1, "K", "C")

        with self.assertRaises((ValueError, InvalidTemperatureError)):
            convertir_temperatura(-0.01, "K", "F")

        with self.assertRaises((ValueError, InvalidTemperatureError)):
            convertir_temperatura(-50, "Kelvin", "Celsius")

        # Rechaza Kelvin negativo incluso si origen y destino son Kelvin
        with self.assertRaises((ValueError, InvalidTemperatureError)):
            convertir_temperatura(-5, "K", "K")

        # Rechaza conversión cuyo resultado en Kelvin sea menor a 0 (ej. -300 °C = -26.85 K)
        with self.assertRaises((ValueError, InvalidTemperatureError)):
            convertir_temperatura(-300, "C", "K")

        # Kelvin = 0 (cero absoluto) debe ser permitido
        self.assertEqual(convertir_temperatura(0, "K", "C"), -273.15)
        self.assertEqual(convertir_temperatura(0, "K", "K"), 0.0)

    # =========================================================================
    # Caso borde 1: Valor no numérico como entrada (ej. "abc") -> error claro
    # =========================================================================
    def test_valor_no_numerico_lanza_error_claro(self):
        valores_invalidos = ["abc", "cien", "", "   ", None, [], {}, object()]
        for val in valores_invalidos:
            with self.assertRaises((ValueError, TypeError, InvalidTemperatureError)) as ctx:
                convertir_temperatura(val, "C", "F")
            # Verificar que el mensaje de error sea explicativo
            self.assertTrue(len(str(ctx.exception)) > 0)
            self.assertIn("numérico", str(ctx.exception).lower())

        # Probar booleano (en python bool es subclase de int, debe ser rechazado)
        with self.assertRaises((ValueError, TypeError, InvalidTemperatureError)):
            convertir_temperatura(True, "C", "F")

    # =========================================================================
    # Caso borde 2: Mismo valor de entrada y salida (ej. Celsius a Celsius)
    # =========================================================================
    def test_mismo_origen_y_destino_devuelve_mismo_numero(self):
        self.assertEqual(convertir_temperatura(25, "C", "C"), 25.0)
        self.assertEqual(convertir_temperatura(-10.5, "F", "F"), -10.5)
        self.assertEqual(convertir_temperatura(300, "K", "K"), 300.0)
        self.assertEqual(convertir_temperatura(0, "Celsius", "Celsius"), 0.0)
        # Redondeo en caso de decimales largos
        self.assertEqual(convertir_temperatura(25.456, "C", "C"), 25.46)

    # =========================================================================
    # Caso borde 3: Números negativos válidos en Celsius/Fahrenheit
    # =========================================================================
    def test_numeros_negativos_validos_se_procesan_sin_problema(self):
        # Punto de coincidencia entre escalas Celsius y Fahrenheit (-40)
        self.assertEqual(convertir_temperatura(-40, "C", "F"), -40.0)
        self.assertEqual(convertir_temperatura(-40, "F", "C"), -40.0)

        # Temperaturas bajo cero habituales
        self.assertEqual(convertir_temperatura(-10, "C", "F"), 14.0)
        self.assertEqual(convertir_temperatura(14, "F", "C"), -10.0)
        self.assertEqual(convertir_temperatura(-10, "C", "K"), 263.15)
        self.assertEqual(convertir_temperatura(-20, "Celsius", "Fahrenheit"), -4.0)

        # Cero absoluto expresado en Celsius y Fahrenheit
        self.assertEqual(convertir_temperatura(-273.15, "C", "K"), 0.0)
        self.assertEqual(convertir_temperatura(-459.67, "F", "K"), 0.0)

    # =========================================================================
    # Soporte de formatos flexibles y aliases
    # =========================================================================
    def test_unidades_case_insensitive_y_simbolos(self):
        self.assertEqual(convertir_temperatura(100, "c", "f"), 212.0)
        self.assertEqual(convertir_temperatura(100, "CELSIUS", "FAHRENHEIT"), 212.0)
        self.assertEqual(convertir_temperatura(100, "°C", "°F"), 212.0)
        self.assertEqual(convertir_temperatura(273.15, "°K", "°C"), 0.0)
        self.assertEqual(convertir_temperatura(0, Unit.CELSIUS, Unit.FAHRENHEIT), 32.0)

    def test_string_numerico_como_entrada(self):
        # Strings que sí representan números válidos deben poder procesarse
        self.assertEqual(convertir_temperatura("100", "C", "F"), 212.0)
        self.assertEqual(convertir_temperatura("-40.0", "C", "F"), -40.0)

    def test_unidad_invalida_lanza_error(self):
        with self.assertRaises((ValueError, InvalidTemperatureError)):
            convertir_temperatura(100, "X", "C")
        with self.assertRaises((ValueError, InvalidTemperatureError)):
            convertir_temperatura(100, "C", "RANKINE")

    # =========================================================================
    # Funciones auxiliares de conveniencia
    # =========================================================================
    def test_funciones_auxiliares(self):
        self.assertEqual(celsius_a_fahrenheit(0), 32.0)
        self.assertEqual(celsius_to_fahrenheit(100), 212.0)
        self.assertEqual(fahrenheit_a_celsius(32), 0.0)
        self.assertEqual(fahrenheit_to_celsius(212), 100.0)
        self.assertEqual(celsius_a_kelvin(0), 273.15)
        self.assertEqual(celsius_to_kelvin(100), 373.15)
        self.assertEqual(kelvin_a_celsius(273.15), 0.0)
        self.assertEqual(kelvin_to_celsius(373.15), 100.0)
        self.assertEqual(fahrenheit_a_kelvin(32), 273.15)
        self.assertEqual(fahrenheit_to_kelvin(212), 373.15)
        self.assertEqual(kelvin_a_fahrenheit(273.15), 32.0)
        self.assertEqual(kelvin_to_fahrenheit(373.15), 212.0)

        # Alias en inglés
        self.assertEqual(convert_temperature(100, "C", "F"), 212.0)


if __name__ == "__main__":
    unittest.main()
