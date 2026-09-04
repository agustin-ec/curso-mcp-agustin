Casos de prueba

| Tipo de caso | Qué es | Comando | Resultado|
| Caso normal | Un uso típico y esperado | python3 converter.py 40 C F | 40 °C = 104.0 °F |
| Caso borde de tu spec | Un caso controlado | python3 converter.py -1 K C | Error: Temperatura en Kelvin inválida: no puede ser menor a 0 (cero absoluto). Se recibió: -1.0 |
| Caso no contemplado | NO incluido en la spec | 104 ºF a ºK | python3 converter.py 104 F K | 104 °F = 313.15 °K |
| Caso normal | Un uso típico y esperado | 313 ºK a ºC | python3 converter.py 313 K C | 313 °K = 39.85 °C |




