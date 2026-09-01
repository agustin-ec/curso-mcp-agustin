## Environment check — Class 1

| Component | Status | Detail |
| :--- | :---: | :--- |
| Python 3.12 | OK | 3.12.3 |
| uv | OK | uv 0.12.6 |
| Git | OK | git version 2.43.0 |
| Docker | OK | Docker version 29.7.2 |
| .gitignore protects .env | OK | protects .env |

Environment ready. See you in Class 2.

## Clase 2 — APIs de IA Generativa y memoria conversacional

**Qué se implementó:** `gemini_client.py` hace la llamada básica a Gemini con `system_instruction`, `temperature` y `max_output_tokens` explícitos, revisando `total_token_count` y `finish_reason` en cada respuesta. `conversation.py` agrega memoria conversacional: se probó una conversación de 8 turnos que recordó correctamente en el turno 8 un dato mencionado en el turno 1 (nombre y color favorito). Los errores `ClientError 429` y `ServerError` (se provocó un 503 real) se capturan por separado y se manejan con reintento y backoff exponencial (1s, 2s, 4s), sin que el programa se detenga.

**Estrategia de memoria elegida: ventana deslizante (`MAX_TURNS = 10`).**
Se reenvían solo los últimos 10 turnos en cada llamada. Para una conversación corta esto equivale a historial completo, pero evita que el costo y el tamaño del contexto crezcan sin límite en conversaciones largas. Se comprobó en una demo aparte (`demo_forgetting`, no incluida en la entrega calificada) que con una ventana más pequeña (`MAX_TURNS = 3`) el modelo pierde datos anteriores al recortarse el historial — evidencia directa del costo de esta estrategia.

**Nota sobre el modelo:** se usó `gemini-3.5-flash-lite` en vez de
`gemini-2.5-flash` porque Google bloqueó este último para API keys nuevas antes de su fecha oficial de baja (16 de octubre de 2026).

**Nota sobre el límite de solicitudes:** por el mismo cambio de modelo (mayor RPM en el tier gratuito), se ajustó `trigger_rate_limit()` de 20 a 30 llamadas para provocar el límite dentro del mismo minuto.
