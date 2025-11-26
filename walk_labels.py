import os
import json

# Ruta base donde se descargó SoccerNet
SN_PATH = r"C:\SoccerNetData"

def main():
    print(">>> Ejecutando walk_labels.py")
    print("Buscando Labels-v3.json dentro de:", SN_PATH)

    labels_path = None

    # Recorremos recursivamente todas las carpetas bajo SN_PATH
    for root, dirs, files in os.walk(SN_PATH):
        # Descomenta esta línea si quieres ver qué carpetas recorre:
        # print("Revisando carpeta:", root)
        if "Labels-v3.json" in files:
            labels_path = os.path.join(root, "Labels-v3.json")
            break

    if labels_path is None:
        print("No se encontró ningún archivo Labels-v3.json en", SN_PATH)
        return

    print("Labels file found at:", labels_path)

    # Cargamos el JSON para ver su estructura
    with open(labels_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    print("Keys in Labels JSON:", list(data.keys())[:10])

    if "annotations" in data:
        print("Número de anotaciones:", len(data["annotations"]))
        print("Ejemplo de anotación:", data["annotations"][0])
    else:
        print("No se encontró la clave 'annotations' en el JSON.")

    print("Preview complete.")

if __name__ == "__main__":
    main()
