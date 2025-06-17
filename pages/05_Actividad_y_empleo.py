import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from src.utils.constants import diccionario_aglomerados, DATA_OUT_PATH
from src.functions_streamlit.empleo import obtener_estadisticas_empleo

st.title("Actividad y Empleo")

INDIVIDUAL_PROCESADO_PATH = DATA_OUT_PATH / "individual_process.csv"

@st.cache_data
def cargar_datos():
    return pd.read_csv(INDIVIDUAL_PROCESADO_PATH, sep=';')

df = cargar_datos()

nombres_aglomerados = list(diccionario_aglomerados.values())

nombre_seleccionado = st.selectbox("Seleccione un aglomerado", [""] + nombres_aglomerados)

def codigo_por_nombre(nombre):
    for codigo, nom in diccionario_aglomerados.items():
        if nom == nombre:
            return codigo
    return None

if nombre_seleccionado:
    codigo_seleccionado = codigo_por_nombre(nombre_seleccionado)

    porcentaje_ocupados, labels, sizes = obtener_estadisticas_empleo(df, codigo_seleccionado)

    st.markdown(f"### Porcentaje de población ocupada en {nombre_seleccionado}: **{porcentaje_ocupados}%**")

    if sizes:
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        st.pyplot(fig)
    else:
        st.write("No hay datos de empleo para mostrar.")
else:
    st.write("Por favor, seleccione un aglomerado para visualizar los datos.")
