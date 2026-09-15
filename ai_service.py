import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL"),
    default_headers={
        "x-opencode-session": "task-manager-session",
        "User-Agent": "task-manager/1.0",
    },
)


def create_simple_tasks(description):
    if not client.api_key:
        return ["Error: La API key no está configurada."]

    prompt = f"""Desglosa la siguiente tarea compleja en una lista de 3 a 5 subtareas simples y accionables.

Tarea: {description}

Formato de respuesta:
- Subtarea 1
- Subtarea 2
- Subtarea 3
- etc.



Responde solo con la lista de subtareas, una por línea, empezando cada línea con un guión.
"""

    try:
        params = {
            "model": "gpt-5.6-luna",
            "instructions": "Eres un asistente experto en gestión de tareas que ayuda a dividir tareas complejas en pasos simples y accionables.",
            "input": prompt,
            "max_output_tokens": 300,
        }

        response = client.responses.create(**params)

        content = response.output_text.strip()
        subtasks = []

        for line in content.splitlines():
            line = line.strip()
            if line.startswith("-"):
                subtask = line[1:].strip()
                if subtask:
                    subtasks.append(subtask)

        return subtasks if subtasks else ["Error: No se han podido generar las subtareas."]

    except Exception as error:
        return [f"Error: No se ha podido realizar la conexión: {error}"]
