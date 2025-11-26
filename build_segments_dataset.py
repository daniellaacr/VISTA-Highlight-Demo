import os
import json
import math
import pandas as pd


SN_PATH = r"C:\SoccerNetData"

HIGHLIGHT_LABELS = {
    "Goal",
    "Shot on target",
    "Penalty",
    "Free-kick",
    "Direct free-kick",
    "Corner",
    "Yellow card",
    "Red card",
    "Shot",
    "Challenge",
}

def parse_game_time(game_time_str: str) -> int:
    """
    Convierte un gameTime del estilo '1 - 04:31' a segundos totales de partido.
    Asumimos tiempos oficiales: 45 min por tiempo.
    """
    try:
        half_str, clock_str = game_time_str.split("-")
        half = int(half_str.strip())
        minutes_str, seconds_str = clock_str.strip().split(":")
        minutes = int(minutes_str)
        seconds = int(seconds_str)

        base = (half - 1) * 45 * 60  # 0 para 1er tiempo, 45*60 para el 2do
        return base + minutes * 60 + seconds
    except Exception:
        return -1  # por si algo raro viene en el JSON


def process_labels_json(labels_path: str):
    """
    Lee un archivo Labels-v3.json / labels-v3.json y devuelve una lista de filas
    con features + etiqueta highlight.
    """
    rows = []

    with open(labels_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    actions = data.get("actions", {})

    for img_name, info in actions.items():
        meta = info.get("imageMetadata", {})
        bboxes = info.get("bboxes", [])
        label = meta.get("label", "")
        visibility = meta.get("visibility", "")
        width = meta.get("width", 1920)
        height = meta.get("height", 1080)
        game_time = meta.get("gameTime", "1 - 00:00")
        game_id = meta.get("gameID", -1)
        half = meta.get("half", 1)
        localpath = meta.get("localpath", "")

    
        t_sec = parse_game_time(game_time)

        # 2) número de jugadores anotados en la imagen
        num_players = 0
        areas = []
        for box in bboxes:
            cls = box.get("class", "")
            if "Player" in cls:
                num_players += 1

            pts = box.get("points", {})
            x1 = pts.get("x1", 0)
            y1 = pts.get("y1", 0)
            x2 = pts.get("x2", 0)
            y2 = pts.get("y2", 0)

            w = max(0, x2 - x1)
            h = max(0, y2 - y1)
            areas.append(w * h)

        # 3) área promedio normalizada de las cajas (si existe)
        if areas:
            mean_area = sum(areas) / len(areas)
            norm_mean_area = mean_area / float(width * height)
        else:
            norm_mean_area = 0.0

        # 4) flag de visibilidad del balón / jugada
        ball_visible = 1 if "visible" in visibility.lower() else 0

        # 5) número total de cajas (jugadores + otras cosas)
        num_boxes = len(bboxes)

        # 1 si es una jugada "importante" según la lista,
        # 0 si es algo más rutinario (throw-in, ball out of play, etc.)
        is_highlight = 1 if label in HIGHLIGHT_LABELS else 0

        row = {
            "game_id": game_id,
            "half": half,
            "game_time_sec": t_sec,
            "label_text": label,
            "localpath": localpath,
            "num_players": num_players,
            "num_boxes": num_boxes,
            "norm_mean_area": norm_mean_area,
            "ball_visible": ball_visible,
            "highlight": is_highlight,
        }

        rows.append(row)

    return rows


def build_dataset(max_games: int = 5):
    """
    Recorre C:\SoccerNetData, encuentra hasta max_games archivos Labels-v3.json
    y construye un DataFrame con todas las acciones.
    """
    all_rows = []
    games_processed = 0

    print(f"[INFO] Buscando archivos Labels-v3.json dentro de: {SN_PATH}")

    for root, dirs, files in os.walk(SN_PATH):
        labels_file = None
        if "Labels-v3.json" in files:
            labels_file = "Labels-v3.json"
        elif "labels-v3.json" in files:
            labels_file = "labels-v3.json"

        if labels_file is not None:
            full_path = os.path.join(root, labels_file)
            print(f"[INFO] Procesando: {full_path}")
            rows = process_labels_json(full_path)
            all_rows.extend(rows)
            games_processed += 1

            if games_processed >= max_games:
                break

    if not all_rows:
        print("[WARN] No se encontraron acciones. Revisa SN_PATH.")
        return

    df = pd.DataFrame(all_rows)
    print(f"[INFO] Total de acciones recogidas: {len(df)}")
    print(df.head())

    out_csv = "soccer_segments_dataset.csv"
    df.to_csv(out_csv, index=False)
    print(f"[OK] Dataset guardado en: {out_csv}")


if __name__ == "__main__":
   
    build_dataset(max_games=5)
