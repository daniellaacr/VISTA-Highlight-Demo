import os
import json

SN_PATH = r"C:\SoccerNetData"


def find_labels_json():
    """Busca el primer labels-v3.json dentro de C:\SoccerNetData."""
    for root, dirs, files in os.walk(SN_PATH):
        # Algunos partidos lo tienen con l minúscula, otros con L mayúscula
        for name in ("labels-v3.json", "Labels-v3.json"):
            if name in files:
                return os.path.join(root, name)
    return None


def main():
    print('"""Busca el primer labels-v3.json dentro de C:\\SoccerNetData."""')
    print("Buscando algún archivo labels-v3.json en:", SN_PATH)
    labels_path = find_labels_json()

    if labels_path is None:
        print("No se encontró labels-v3.json en el dataset.")
        return

    print("\nUsando este archivo:\n", labels_path, "\n")

    with open(labels_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Vemos las claves principales del JSON
    keys = list(data.keys())
    print("Keys en el JSON:", keys)

    actions = data.get("actions", None)

    if actions is None:
        print("Este JSON no tiene clave 'actions'.")
        return

    print("\nTipo de 'actions':", type(actions))

    # Caso 1: actions es una lista
    if isinstance(actions, list):
        print("Número de acciones anotadas:", len(actions))

        print("\nPrimeras 5 acciones:")
        for a in actions[:5]:
            print(a)

    # Caso 2: actions es un diccionario
    elif isinstance(actions, dict):
        action_keys = list(actions.keys())
        print("Número de llaves en 'actions':", len(action_keys))
        print("Primeras llaves:", action_keys[:5])

        first_key = action_keys[0]
        print("\nMostrando contenido para la llave:", first_key)
        first_val = actions[first_key]
        print("Tipo del valor asociado:", type(first_val))

        # Si el valor asociado es lista, mostramos primeros elementos
        if isinstance(first_val, list):
            print("\nPrimeros elementos de esa lista:")
            for a in first_val[:5]:
                print(a)
        else:
            print("\nContenido de esa entrada:")
            print(first_val)
    else:
        print("Formato de 'actions' no esperado:", type(actions))

    print("\nPreview completa.")


if __name__ == "__main__":
    main()
