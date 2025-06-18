"""Pagina 06. Funciones educativas"""
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import json
from src.dataset.consultar_dataset import ranking_aglomerado_EJ4

def procesar_niveles_educativos(df, año_seleccionado):
    """Procesa los datos educativos y devuelve un DataFrame con conteos ponderados"""
    nivel_educativo_map = {
        1: "Primario Incompleto",
        2: "Primario Completo",
        3: "Secundario Incompleto",
        4: "Secundario Completo",
        5: "Superior universitario incompleto",
        6: "Superior universitario Completo",
        7: "Sin Instrucción",
        9: "Ns/Nr"
    }
    
    df["NIVEL_ED_TEXTO"] = df["NIVEL_ED"].map(nivel_educativo_map)
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