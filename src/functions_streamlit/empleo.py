"""Pagina 05. Funciones para empleo y actividad"""
import pandas as pd
import json
import streamlit as st

@st.cache_data
def cargar_datos(path):
    columnas = ['ANO4', 'TRIMESTRE', 'NIVEL_ED', 'ESTADO', 'PONDERA']
    try:
        df = pd.read_csv(
            path,
            sep=";",
            decimal=",",
            usecols=columnas,
            dtype={
                'ANO4': 'int16',
                'TRIMESTRE': 'int8',
                'NIVEL_ED': 'int8',
                'ESTADO': 'int8',
                'PONDERA': 'float32'
            }
        )
        return df
    except Exception as e:
        st.error(f"Error al cargar datos: {str(e)}")
        return None

@st.cache_data
def cargar_metadata(ruta):
    try:
        with open(ruta, 'r') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error al cargar metadatos: {str(e)}")
        return {}

def mapear_nivel_educativo(serie_nivel_ed, valores):
    nivel_educativo_map = {
        1: "Primario incompleto",
        2: "Primario completo", 
        3: "Secundario incompleto",
        4: "Secundario completo",
        5: "Superior universitario incompleto",
        6: "Superior universitario completo",
        7: "Sin instrucción",
        9: "Ns/Nr"
    }
    return serie_nivel_ed.rename(index=nivel_educativo_map).sort_index()

def format_number(x):
    if isinstance(x, (int, float)):
        return f"{x:,.0f}".replace(",", ".") if x == int(x) else f"{x:,.1f}".replace(",", ".")
    return x
