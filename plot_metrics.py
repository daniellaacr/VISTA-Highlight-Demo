import matplotlib.pyplot as plt

# ------- Datos por fold que tú obtuviste -------
ap = [0.2679, 0.1458, 0.3026, 0.5531, 0.4787]
precision = [0.0, 0.0, 0.20, 1.0, 1.0]
recall = [0.0, 0.0, 0.5, 0.1667, 0.1667]

folds = [1, 2, 3, 4, 5]

# ---------- 1. Gráfica AP ----------
plt.figure(figsize=(6,4))
plt.plot(folds, ap, marker="o", linewidth=2)
plt.title("Average Precision por Fold")
plt.xlabel("Fold")
plt.ylabel("Average Precision")
plt.grid(True)
plt.savefig("ap_fold.png", dpi=300)
plt.close()

# ---------- 2. Gráfica Precision ----------
plt.figure(figsize=(6,4))
plt.plot(folds, precision, marker="o", color="green", linewidth=2)
plt.title("Precision por Fold")
plt.xlabel("Fold")
plt.ylabel("Precision")
plt.grid(True)
plt.savefig("precision_fold.png", dpi=300)
plt.close()

# ---------- 3. Gráfica Recall ----------
plt.figure(figsize=(6,4))
plt.plot(folds, recall, marker="o", color="red", linewidth=2)
plt.title("Recall por Fold")
plt.xlabel("Fold")
plt.ylabel("Recall")
plt.grid(True)
plt.savefig("recall_fold.png", dpi=300)
plt.close()

print("Gráficas generadas: ap_fold.png, precision_fold.png, recall_fold.png")
