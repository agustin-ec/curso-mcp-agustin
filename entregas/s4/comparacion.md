## Comparación:

| Aspecto | Spec a mano | Spec Kit |
| ¿Cubrió los mismos casos borde? | Sí, los que se escribieron explícitamente (Kelvin < 0, no numérico, identidad, negativos válidos). | Sí, y además generó casos borde que la spec manual no contempló: rechazo de Celsius/Fahrenheit por debajo del cero absoluto (no solo Kelvin), decimales periódicos, punto de coincidencia (-40°), y precisión en conversiones de ida y vuelta. |
| ¿Qué generó Spec Kit que tú no habías escrito? | — | Historias de usuario con prioridades (P1/P2/P3), 8 requisitos funcionales formales (FR-001 a FR-008), entidades clave del dominio, y 4 criterios de éxito medibles (ej. "conversión en menos de 10ms"). También 25 pruebas automatizadas frente a las 11 de la spec manual. |
| ¿Qué se sintió más rápido de arrancar? | Spec a mano: 3 secciones cortas y en minutos ya tenía código funcionando con `agy`. | Más lento para arrancar: instalar `specify-cli` y correr 4 comandos secuenciales (`specify → plan → tasks → implement`) antes de tener código. |
| ¿Cuál te generó más confianza en el resultado? |  | Por la cantidad de pruebas automatizadas (25) y por cubrir casos físicos que mi spec manual nunca pensó (como validar límites en Celsius/Fahrenheit, no solo en Kelvin). |

## Frase de cierre:

La próxima vez que tenga un proyecto de tamaño pequeño, elegiría spec a mano porque es más rápido de escribir y no necesito el nivel de formalidad de historias de usuario y criterios de éxito medibles; pero para un proyecto mediano o grande, elegiría Spec Kit porque su cobertura de casos borde y sus pruebas automáticas dan mucha más confianza en sistemas donde un error saldría caro.


