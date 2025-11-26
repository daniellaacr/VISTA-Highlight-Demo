import pandas as pd
from sklearn.model_selection import KFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import average_precision_score, precision_recall_fscore_support
from joblib import dump

DATASET_CSV = "soccer_segments_dataset.csv"
MODEL_PATH = "highlight_model.joblib"


def train_with_cv(X, y):
    kf = KFold(n_splits=5, shuffle=True, random_state=42)

    ap_scores = []
    prec_scores = []
    rec_scores = []

    fold = 1
    for train_idx, test_idx in kf.split(X):
        X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
        y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

        model = RandomForestClassifier(
            n_estimators=200,
            max_depth=None,
            random_state=42,
            n_jobs=-1,
        )

        model.fit(X_train, y_train)

        # Probabilidad de clase positiva
        y_proba = model.predict_proba(X_test)[:, 1]
        y_pred = model.predict(X_test)

        ap = average_precision_score(y_test, y_proba)
        precision, recall, f1, _ = precision_recall_fscore_support(
            y_test, y_pred, average="binary", zero_division=0
        )

        print(f"\n[FOLD {fold}]")
        print("  Average Precision:", round(ap, 4))
        print("  Precision:", round(precision, 4))
        print("  Recall:", round(recall, 4))
        print("  F1:", round(f1, 4))

        ap_scores.append(ap)
        prec_scores.append(precision)
        rec_scores.append(recall)

        fold += 1

    print("\n=== 5-Fold CV Results ===")
    print("Mean Average Precision:", round(sum(ap_scores) / len(ap_scores), 4))
    print("Mean Precision:", round(sum(prec_scores) / len(prec_scores), 4))
    print("Mean Recall:", round(sum(rec_scores) / len(rec_scores), 4))


def main():
    print("[INFO] Cargando dataset:", DATASET_CSV)
    df = pd.read_csv(DATASET_CSV)

    # Nos quedamos con las filas que tengan tiempo válido (> 0)
    df = df[df["game_time_sec"] >= 0].copy()

    feature_cols = ["num_players", "num_boxes", "norm_mean_area", "ball_visible"]
    X = df[feature_cols]
    y = df["highlight"]

    print("[INFO] Total samples:", len(df))
    print("[INFO] Positivos (highlight=1):", y.sum())
    print("[INFO] Negativos (highlight=0):", (y == 0).sum())

    # 1) Entrenamos con 5-fold solo para obtener métricas
    train_with_cv(X, y)

    # 2) Entrenamos un modelo final con TODO el dataset y lo guardamos
    print("\n[INFO] Entrenando modelo final en todo el dataset...")
    final_model = RandomForestClassifier(
        n_estimators=200,
        max_depth=None,
        random_state=42,
        n_jobs=-1,
    )
    final_model.fit(X, y)

    dump(final_model, MODEL_PATH)
    print(f"[OK] Modelo final guardado en: {MODEL_PATH}")


if __name__ == "__main__":
    main()

