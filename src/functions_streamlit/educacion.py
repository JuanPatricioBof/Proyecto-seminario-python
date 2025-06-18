"""Pagina 06. Funciones educativas"""
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import json
from src.dataset.consultar_dataset import ranking_aglomerado_EJ4
import numpy as np
# -------------------- 1.6.1 --------------------
def procesar_niveles_educativos(df, año_seleccionado):
    """Procesa los datos educativos y devuelve un DataFrame con conteos ponderados"""
    df["NIVEL_ED_TEXTO"] = df["NIVEL_ED"].map(NIVEL_EDUCATIVO_MAP)
    df_año = df[df["ANO4"] == año_seleccionado]
    conteo = df_año.groupby("NIVEL_ED_TEXTO")["PONDERA"].sum().reset_index()
    conteo.columns = ["Nivel Educativo", "Cantidad Ponderada"]
    
    return conteo.sort_values("Cantidad Ponderada", ascending=False)

def crear_grafico_barras(conteo, año):
     """Crea y devuelve un gráfico de barras estilizado con solo Matplotlib"""

     colores = plt.cm.Paired.colors[:len(conteo)]

     fig, ax = plt.subplots(figsize=(12, 6), facecolor='#0e1117')
     ax.set_facecolor('#0e1117')

     # Dibujar barras
     bars = ax.bar(
        conteo["Nivel Educativo"],
        conteo["Cantidad Ponderada"],
        color=colores,
        edgecolor='white'
    )

     # Ejes y título con estilo
     ax.set_title(f"Nivel Educativo - Año {año}", fontsize=16, weight='bold', pad=20, color='white')
     ax.set_xlabel("Nivel Educativo", fontsize=12, color='white')
     ax.set_ylabel("Cantidad Ponderada", fontsize=12, color='white')
     ax.tick_params(colors='white')  # ticks blancos

     # Rotar etiquetas X
     ax.set_xticks(range(len(conteo)))
     ax.set_xticklabels(conteo["Nivel Educativo"], rotation=45, ha='right', fontsize=10, color='white')

     # Eje Y formateado
     ax.set_yticklabels([f"{int(t):,}".replace(",", ".") for t in ax.get_yticks()], color='white')

     # Bordes limpios
     ax.spines['top'].set_visible(False)
     ax.spines['right'].set_visible(False)
     ax.spines['left'].set_color('white')
     ax.spines['bottom'].set_color('white')

     # Grilla sutil
     ax.grid(axis='y', linestyle='--', alpha=0.2)

     # Etiquetas en las barras
     ax.bar_label(bars, fmt='%.0f', fontsize=8, label_type='edge', padding=2, rotation=00, color='white')

     plt.tight_layout()
     return plt
 # -------------------- 1.6.2 --------------------
# Constante global para reutilizar en otras funciones
# Mapeo de niveles educativos (con nombre y orden)
NIVEL_EDUCATIVO_MAP = {
    1: "Primario Incompleto",
    2: "Primario Completo",
    3: "Secundario Incompleto",
    4: "Secundario Completo",
    5: "Superior universitario incompleto",
    6: "Superior universitario Completo",
    7: "Sin Instrucción",
    9: "Ns/Nr"
}

INTERVALOS = {
    "20-30": (20, 30),
    "30-40": (30, 40),
    "40-50": (40, 50),
    "50-60": (50, 60),
    "60+": (60, 150)
}


def asignar_intervalo(edad):
    for nombre, (min_, max_) in INTERVALOS.items():
        if min_ <= edad < max_:
            return nombre
    return None


def obtener_nivel_mas_comun_ordinal(df, intervalos_seleccionados):
    df = df.copy()
    df["Intervalo"] = df["CH06"].apply(asignar_intervalo)
    df = df[df["Intervalo"].isin(intervalos_seleccionados)]
    df["NIVEL_ED_TEXTO"] = df["NIVEL_ED"].map(NIVEL_EDUCATIVO_MAP)

    resultado = []
    for intervalo in intervalos_seleccionados:
        df_int = df[df["Intervalo"] == intervalo]
        if df_int.empty:
            resultado.append((intervalo, "Sin datos", 0))
            continue

        nivel_ponderado = (
            df_int.groupby("NIVEL_ED_TEXTO")["PONDERA"].sum()
            .sort_values(ascending=False)
        )

        nivel_mas_comun = nivel_ponderado.idxmax()
        # Buscar clave en el dict original (ordinal)
        ordinal = next((k for k, v in NIVEL_EDUCATIVO_MAP.items() if v == nivel_mas_comun), 0)
        resultado.append((intervalo, nivel_mas_comun, ordinal))


    return pd.DataFrame(resultado, columns=["Intervalo", "Nivel Educativo", "Nivel Ordinal"])


def graficar_nivel_mas_comun_ordinal(df_resultado):
    fig, ax = plt.subplots(figsize=(10, 6), facecolor='#0e1117')
    ax.set_facecolor('#0e1117')

    y_pos = range(len(df_resultado))
    valores = df_resultado["Nivel Ordinal"]
    etiquetas = df_resultado["Intervalo"]
    niveles = df_resultado["Nivel Educativo"]

    colores = plt.cm.Set2.colors[:len(df_resultado)]
    barras = ax.barh(y_pos, valores, color=colores, edgecolor='white')

    ax.set_yticks(y_pos)
    ax.set_yticklabels(etiquetas, color='white', fontsize=11)
    ax.invert_yaxis()

    posiciones = list(NIVEL_EDUCATIVO_MAP.keys())
    nombres = list(NIVEL_EDUCATIVO_MAP.values())
    ax.set_xticks(posiciones)
    ax.set_xticklabels(nombres, rotation=45, ha='right', color='white', fontsize=9)

    ax.set_title("Nivel Educativo Más Común por Intervalo Etario", color='white', fontsize=14, pad=15)
    ax.set_xlabel("Nivel Educativo", color='white')

    for i, bar in enumerate(barras):
        ancho = bar.get_width()
        ax.text(ancho + 0.1, bar.get_y() + bar.get_height()/2,
                niveles.iloc[i], va='center', ha='left', color='white', fontsize=10)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('white')
    ax.spines['bottom'].set_color('white')
    ax.tick_params(colors='white')
    ax.grid(axis='x', linestyle='--', alpha=0.2)
    ax.set_xlim(0, 8.5)

    plt.tight_layout()
    return fig