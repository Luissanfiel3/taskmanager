from task_manager import TaskManager
from ai_service import create_simple_tasks

def print_menu():
    print("\n--- Gestor de Tareas Inteligente ---")
    print("1. Añadir tarea")
    print("2. Añadir tarea compleja (con IA)")
    print("3. Listar tareas")
    print("4. Completar tarea")
    print("5. Eliminar tarea")
    print("6. Salir")

def main():

    manager = TaskManager()

    while True:

        print_menu()

        try:

            choice = int(input("Elige una opción: "))

            match choice:
                case 1:
                    description = input("Descripción de la tarea: ")
                    manager.add_task(description)
                case 2:
                    description = input("Descripción de la tarea compleja: ")
                    subtasks = create_simple_tasks(description)
                    print("\nSubtareas generadas por IA:")
                    for number, subtask in enumerate(subtasks, start=1):
                        if not subtask.startswith("Error:"):
                            print(f"{number}. {subtask}")
                            manager.add_task(subtask)
                        else:
                            print(subtask)
                            break
                case 3:
                    print("Listado de tareas: ")
                    manager.list_task()
                case 4:
                    id = input("ID de la tarea a completar: ")
                    manager.complete_task(id)
                case 5:
                    id = input("ID de la tarea a eliminar: ")
                    manager.delete_task(id)
                case 6:
                    print("Saliendo...")
                    break
                case _:
                    print("Opción no válida. Selecciona otra.")
        except ValueError:
            print("Es una opción no válida")
if __name__ == "__main__":
    main()
