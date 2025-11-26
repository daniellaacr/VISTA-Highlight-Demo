import cv2
import numpy as np
from joblib import load
import argparse
import os
import warnings

# Silenciar warnings molestos de sklearn
warnings.filterwarnings("ignore", category=UserWarning)

MODEL_PATH = "highlight_model.joblib"


def load_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"No se encontró el modelo en: {MODEL_PATH}")

    print(f"[INFO] Cargando modelo: {MODEL_PATH}")
    model = load(MODEL_PATH)
    n_feats = getattr(model, "n_features_in_", "desconocido")
    print(f"[INFO] El modelo espera {n_feats} características de entrada.")
    return model


def extract_features(frame):
    """
    Extrae 3 características sencillas:
    - Intensidad promedio
    - Desviación estándar
    - Número de píxeles de borde (Canny)
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    intensity_mean = float(gray.mean())
    intensity_std = float(gray.std())

    edges = cv2.Canny(gray, 80, 150)
    edge_count = float((edges > 0).sum())

    return gray, [intensity_mean, intensity_std, edge_count]


def run_demo(video_path, max_frames=None):
    model = load_model()
    n_model = getattr(model, "n_features_in_", None)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError(f"No pude abrir el video: {video_path}")

    print("[INFO] Reproduciendo video... presiona 'q' para salir.")

    frame_idx = 0
    prev_gray = None

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("[INFO] Fin del video.")
            break

        frame_idx += 1
        if max_frames is not None and frame_idx > max_frames:
            print(f"[INFO] Parando demo después de {max_frames} frames.")
            break

        # Saltar frames para que vaya más rápido (usa 1 de cada 3)
        if frame_idx % 3 != 0:
            continue

        # Reducir tamaño de la ventana (más fluido, más manejable)
        frame = cv2.resize(frame, (800, 450))

        # 1) Features básicos + gray actual
        gray, feats = extract_features(frame)

        # 2) Score de movimiento basado en diferencia con el frame previo
        if prev_gray is None:
            motion_score = 0.0
        else:
            diff = cv2.absdiff(gray, prev_gray)
            diff_mean = float(diff.mean())
            # normalización muy burda a [0,1]
            motion_score = (diff_mean - 5.0) / (25.0 - 5.0)
            motion_score = float(np.clip(motion_score, 0.0, 1.0))

        prev_gray = gray

        # 3) Ajustar dimensionalidad de features para el modelo
        if n_model is not None:
            if len(feats) < n_model:
                feats = feats + [0.0] * (n_model - len(feats))
            elif len(feats) > n_model:
                feats = feats[:n_model]

        # 4) Probabilidad del RandomForest
        try:
            prob_rf = float(model.predict_proba([feats])[0][1])
        except Exception:
            # por si acaso algo raro pasa, que no truene el demo
            prob_rf = 0.5

        # 5) Combinar modelo + movimiento para que se vea más reactivo
        prob = 0.5 * prob_rf + 0.5 * motion_score

        # ---------------- DIBUJO EN PANTALLA ----------------
        overlay = frame.copy()
        box_w, box_h = 360, 60
        x1, y1 = 10, 10
        x2, y2 = x1 + box_w, y1 + box_h

        # Fondo negro semi-transparente
        cv2.rectangle(overlay, (x1, y1), (x2, y2), (0, 0, 0), -1)
        frame = cv2.addWeighted(overlay, 0.5, frame, 0.5, 0)

        color_text = (0, 255, 0) if prob < 0.6 else (0, 0, 255)
        text = f"Highlight prob: {prob:.2f}"

        cv2.putText(
            frame,
            text,
            (x1 + 15, y1 + 38),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            color_text,
            2,
            cv2.LINE_AA,
        )

        cv2.imshow("Highlight demo", frame)

        # Velocidad: rápido por defecto, más lento cuando sube el score
        if prob >= 0.6:
            delay = 80   # se nota el "highlight" pero no se congela
        else:
            delay = 25   # bastante fluido

        key = cv2.waitKey(delay) & 0xFF
        if key == ord("q"):
            print("[INFO] Demo interrumpida por el usuario.")
            break

    cap.release()
    cv2.destroyAllWindows()
    print("[INFO] Demo terminada.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--video",
        type=str,
        required=True,
        help="Ruta al video de entrada (por ejemplo, el clip de FIFA).",
    )
    args = parser.parse_args()

    run_demo(args.video)
