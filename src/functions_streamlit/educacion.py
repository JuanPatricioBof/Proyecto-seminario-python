"""Pagina 06. Funciones educativas"""
import pandas as pd
import plotly.express as px
from pathlib import Path
import json

def cargar_datos(path):
    """Lée el csv y lo retorna como un DataFrame"""
    return pd.read_csv(path, sep=";", decimal=",", low_memory=False)

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
    """Crea y devuelve un gráfico de barras Plotly"""
    fig = px.bar(
        conteo,
        x="Nivel Educativo",
        y="Cantidad Ponderada",
        color="Nivel Educativo",
        text_auto=True,
        height=500,
        title=f"Nivel Educativo - Año {año}"
    )
    return fig
def cargar_json(path):
    with open(path, 'r') as f:
        fechas = json.load(f)
    return {int(k): [int(vv) for vv in v] for k, v in fechas.items()}