"""Módulo para generar visualmente el diagrama de comportamiento con Matplotlib."""

import matplotlib.pyplot as plt


def crear_diagrama():
    """Genera y guarda el diagrama de comportamiento como imagen PNG."""
    fig, ax = plt.subplots(figsize=(10, 12))
    ax.axis("off")

    # Estilos seguros compatibles con todas las versiones de Matplotlib
    box_blue = dict(
        boxstyle="round,pad=0.5",
        facecolor="#D4E6F1",
        edgecolor="#2980B9",
        lw=1.5
    )
    box_yellow = dict(
        boxstyle="round,pad=0.5",
        facecolor="#FCF3CF",
        edgecolor="#F39C12",
        lw=1.5
    )
    box_green = dict(
        boxstyle="round,pad=0.5",
        facecolor="#D5F5E3",
        edgecolor="#27AE60",
        lw=1.5
    )
    box_red = dict(
        boxstyle="square,pad=0.5",
        facecolor="#FADBD8",
        edgecolor="#C0392B",
        lw=1.5
    )

    pasos = [
        ("Inicio (__main__)", 0.95, box_blue),
        ("1. Llama a cargar_cache()", 0.87, box_blue),
        ("Genera conjunto urls_existentes", 0.79, box_blue),
        ("2. Llama a extractor_facebook_apify()", 0.71, box_blue),
        ("Petición POST a Apify", 0.63, box_yellow),
        ("¿Respuesta HTTP 200/201?", 0.53, box_red),
        ("Itera items obtenidos", 0.43, box_yellow),
        (
            "_obtener_fecha_y_dia() | extraer_ubicacion_del_texto()",
            0.33,
            box_green
        ),
        ("¿Nuevos registros no guardados?", 0.23, box_red),
        ("3. Llama a guardar_cache()", 0.13, box_yellow),
        ("Fin de ejecución", 0.03, box_blue),
    ]

    # Dibujar cajas y textos
    for texto, y_pos, estilo in pasos:
        ax.text(
            0.5, y_pos, texto,
            ha="center", va="center",
            fontsize=10, weight="bold",
            bbox=estilo
        )

    # Dibujar flechas
    arrow_props = dict(arrowstyle="->", lw=1.5, color="#34495E")
    for i in range(len(pasos) - 1):
        y_top = pasos[i][1] - 0.03
        y_bottom = pasos[i + 1][1] + 0.03
        ax.annotate(
            "",
            xy=(0.5, y_bottom),
            xytext=(0.5, y_top),
            arrowprops=arrow_props
        )

    plt.tight_layout()
    plt.savefig("diagrama_codigo.png", dpi=300, bbox_inches="tight")
    print("¡Diagrama generado con éxito como 'diagrama_codigo.png'!")


if __name__ == "__main__":
    crear_diagrama()