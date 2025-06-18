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
    """Crea y devuelve un gráfico de barras con Matplotlib"""
    # Configuración del gráfico
    plt.figure(figsize=(12, 6))
    bars = plt.bar(
        conteo["Nivel Educativo"],
        conteo["Cantidad Ponderada"],
        color=plt.cm.tab20.colors[:len(conteo)]  # Usar colores distintos
    )
    
    # Añadir etiquetas y título
    plt.title(f"Nivel Educativo - Año {año}", fontsize=14, pad=20)
    plt.xlabel("Nivel Educativo", fontsize=12)
    plt.ylabel("Cantidad Ponderada", fontsize=12)
    
    # Rotar etiquetas del eje x para mejor legibilidad
    plt.xticks(rotation=45, ha='right', fontsize=10)
    
    # Añadir valores en las barras
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width()/2., 
            height,
            f'{int(height):,}',
            ha='center',
            va='bottom',
            fontsize=9
        )
    
    # Ajustar márgenes
    plt.tight_layout()
    
    return plt