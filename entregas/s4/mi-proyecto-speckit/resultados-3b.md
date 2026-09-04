Casos de prueba

| Tipo de caso | Qué es | Comando | Resultado spec a mano | Resultado Spec Kit |
| Caso normal | Un uso típico y esperado | python3 -m src.cli 40 -f C -t F | 104 | 104 |
| Caso borde de tu spec | Un caso controlado | python3 -m src.cli -1 -f K -t C  | Error | Error |
| Caso no contemplado | NO incluido en la spec | python3 -m src.cli 104 -f F -t K  | 313.15 | 313.15 |
| Caso normal | Un uso típico y esperado | python3 -m src.cli 313.15 -f K -t C  | 39.85 | 40 |





