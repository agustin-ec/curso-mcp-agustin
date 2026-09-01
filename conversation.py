"""In-memory conversation history — the model 'remembers' because we resend it."""

import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import errors, types

load_dotenv()

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

MODEL = "gemini-3.5-flash-lite"
SYSTEM_INSTRUCTION = "Eres un asistente breve. Respondes en español."

# List of plain dicts, same shape as `contents` — nothing hidden here.
history: list[dict] = []

MAX_TURNS = 10  # conserva los últimos 10 intercambios usuario/modelo (20 entradas)


def trim_history() -> None:
    max_entries = MAX_TURNS * 2
    if len(history) > max_entries:
        del history[:-max_entries]

def send(message: str, _retries: int = 0) -> str:
    trim_history()
    history.append({"role": "user", "parts": [{"text": message}]})

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=history,
            config=types.GenerateContentConfig(system_instruction=SYSTEM_INSTRUCTION),
        )
    except errors.ClientError as exc:
        if exc.code == 429 and _retries < 3:
            wait = 2 ** _retries
            print(f"[429] Límite de RPM alcanzado. Reintentando en {wait}s...")
            time.sleep(wait)
            history.pop()  # evita duplicar el mismo turno de usuario
            return send(message, _retries=_retries + 1)
        history.pop()
        return f"Error del cliente ({exc.code}): {exc.message}. No se reintenta."
    except errors.ServerError as exc:
        if _retries < 3:
            wait = 2 ** _retries
            print(f"[{exc.code}] Error del servidor. Reintentando en {wait}s...")
            time.sleep(wait)
            history.pop()
            return send(message, _retries=_retries + 1)
        history.pop()
        return f"El servicio no respondió tras varios intentos ({exc.code})."

    finish_reason = str(response.candidates[0].finish_reason)
    if "MAX_TOKENS" in finish_reason:
        print("[warning] Respuesta truncada por max_output_tokens.")

    history.append({"role": "model", "parts": [{"text": response.text}]})
    return response.text


def main() -> None:
    # 8 turnos: el dato va en el turno 1, y se pregunta de vuelta en el turno 8.
    print(send("Me llamo Alex y mi color favorito es el verde."))
    print(send("¿Qué framework de Python vimos en la Clase 1?"))
    print(send("Dame un ejemplo de dato que no cabe en un int."))
    print(send("¿Qué hace el comando uv init?"))
    print(send("Explica en una frase qué es un token."))
    print(send("¿Qué significa que una API sea stateless?"))
    print(send("¿Para qué sirve un archivo .env?"))
    print(send("¿Cómo me llamo y cuál es mi color favorito?"))

def demo_forgetting() -> None:
    """Standalone demo: a short window forgets the beginning. Not part of the graded run."""
    global history, MAX_TURNS
    history = []
    original_max = MAX_TURNS
    MAX_TURNS = 3  # pequeño a propósito, para forzar el olvido

    print(send("Mi mascota se llama Rocko."))
    for i in range(1, 7):
        print(send(f"Pregunta de relleno número {i}."))
    print(send("¿Cómo se llama mi mascota?"))  # ya se cayó de la ventana

    MAX_TURNS = original_max
    history = []

def trigger_rate_limit() -> None:
    """Sends several requests back to back to hit the free tier's requests-per-minute cap."""
    global history
    history = []
    for i in range(1, 31):
        print(f"Request {i}: {send(f'Cuenta hasta {i}.')}")

if __name__ == "__main__":
    main()
