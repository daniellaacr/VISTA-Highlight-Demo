import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrow

# --------------------------------------------------------
# Diagrama sencillo del pipeline VISTA / Soccer highlight
# --------------------------------------------------------

def draw_box(ax, xy, text, box_color="#82b1ff"):
    """
    Dibuja una caja redondeada con texto.
    xy = (x, y) esquina inferior izquierda
    """
    x, y = xy
    width, height = 2.8, 1.2

    box = FancyBboxPatch(
        (x, y),
        width,
        height,
        boxstyle="round,pad=0.2",
        linewidth=2,
        edgecolor="black",
        facecolor=box_color,
    )
    ax.add_patch(box)

    ax.text(
        x + width / 2,
        y + height / 2,
        text,
        ha="center",
        va="center",
        fontsize=10,
        wrap=True,
    )

    # Devuelve el centro de la caja para poder conectar flechas
    return x + width, y + height / 2


def main():
    fig, ax = plt.subplots(figsize=(11, 3))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 3)
    ax.axis("off")

    # 1. Input video
    x1, y1 = 0.5, 1.0
    right1, center1 = draw_box(
        ax,
        (x1, y1),
        "Input video\n(FIFA match clip)",
        box_color="#82b1ff",
    )

    # 2. Preprocesamiento
    x2 = right1 + 0.6
    right2, center2 = draw_box(
        ax,
        (x2, y1),
        "Preprocessing\n(Resize, Gray)",
        box_color="#b3d9ff",
    )

    # 3. Extracción de características
    x3 = right2 + 0.6
    right3, center3 = draw_box(
        ax,
        (x3, y1),
        "Feature Extraction\n(mean, std, edge count)",
        box_color="#c8e6c9",
    )

    # 4. Modelo de highlight
    x4 = right3 + 0.6
    right4, center4 = draw_box(
        ax,
        (x4, y1),
        "Highlight model\n(Random Forest, 5-fold CV)",
        box_color="#ffe082",
    )

    # 5. Salida
    x5 = right4 + 0.6
    right5, center5 = draw_box(
        ax,
        (x5, y1),
        "Output video +\nHighlight probability\n(y slowed when high)",
        box_color="#ffccbc",
    )

    # Flechas entre cajas
    centers = [center1, center2, center3, center4]
    rights = [right1, right2, right3, right4]
    for r, c in zip(rights, centers):
        arrow = FancyArrow(
            r + 0.05,
            c,
            0.5,
            0.0,
            width=0.03,
            length_includes_head=True,
            head_width=0.15,
            head_length=0.25,
            color="black",
        )
        ax.add_patch(arrow)

    plt.tight_layout()
    plt.savefig("pipeline_diagram.png", dpi=300)
    print("Pipeline diagram saved as: pipeline_diagram.png")


if __name__ == "__main__":
    main()
