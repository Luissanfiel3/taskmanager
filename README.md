# Gestor de Tareas Inteligente

Aplicación de consola en Python para gestionar tareas diarias, con apoyo de inteligencia artificial para desglosar tareas complejas en subtareas simples y accionables.

## Características

- Añadir tareas con descripción personalizada.
- Añadir tareas complejas y generar automáticamente de 3 a 5 subtareas mediante IA.
- Listar todas las tareas guardadas.
- Completar tareas por ID.
- Eliminar tareas por ID.
- Persistencia en JSON (`Task.json`), con IDs consecutivos que se restauran al cargar.

## Requisitos

- Python 3.10 o superior (se recomienda 3.14).
- Una suscripción de OpenCode Go con su API key.
- Dependencias del proyecto:

```text
openai
python-dotenv
```

## Instalación

1. Clona o descarga el proyecto.
2. Crea y activa un entorno virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Instala las dependencias:

```powershell
python -m pip install -r requirements.txt
```

## Configuración

Crea un archivo `.env` en la raíz del proyecto:

```env
OPENAI_API_KEY=tu_clave_de_opencode_go
OPENAI_BASE_URL=https://opencode.ai/zen/go/v1
```

Notas:

- La URL base debe terminar en `/v1`; el SDK añade `/responses` automáticamente.
- El modelo usado es `gpt-5.6-luna` mediante la Responses API.
- OpenCode Go requiere las cabeceras `x-opencode-session` y un `User-Agent` propio; el cliente ya las envía.
- `.env` está incluido en `.gitignore`; no subas tu API key al repositorio.

## Uso

Ejecuta el programa:

```powershell
python main.py
```

Menú disponible:

```text
1. Añadir tarea
2. Añadir tarea compleja (con IA)
3. Listar tareas
4. Completar tarea
5. Eliminar tarea
6. Salir
```

Ejemplo con IA: al elegir la opción 2 e introducir "Quiero estudiar terapia ocupacional desde cero", el programa genera y guarda subtareas numeradas:

```text
Subtareas generadas por IA:
1. Investigar qué es la terapia ocupacional...
2. Reunir recursos introductorios fiables...
3. Estudiar las bases de anatomía...
```

## Estructura del proyecto

```text
task-manager/
├── main.py               # Menú e interacción con el usuario
├── task_manager.py       # Clases Task y TaskManager (lógica y persistencia)
├── ai_service.py         # Cliente de IA compatible con OpenAI (OpenCode Go)
├── test_task_manager.py  # Tests unitarios del TaskManager
├── Task.json             # Almacenamiento de tareas (se crea automáticamente)
├── requirements.txt      # Dependencias
└── .env                  # Claves de configuración (no se sube a Git)
```

## Tests

La suite de tests usa archivos temporales, por lo que nunca modifica tu `Task.json` real:

```powershell
python -m unittest test_task_manager.py -v
```

Cobertura actual (9 tests):

- Inicio sin archivo de tareas.
- Añadir tarea y persistencia en JSON.
- Carga de tareas y restauración del siguiente ID.
- Simulación de carga con datos de prueba.
- Completar y eliminar tareas existentes.
- IDs inexistentes no alteran las tareas.
- IDs no numéricos lanzan `ValueError`.

## Notas técnicas

- `Task.__str__` usa `X` como marcador de tarea completada para evitar problemas de codificación en consolas Windows (`cp1252`).
- Si la API de IA falla, el programa muestra un mensaje de error sin romper el flujo del menú.
- Los errores de la IA empiezan siempre por `Error:`, lo que permite filtrarlos en el menú.
