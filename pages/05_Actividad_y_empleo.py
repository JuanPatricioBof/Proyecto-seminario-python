import streamlit as st
import pandas as pd
import json
import folium
from streamlit_folium import st_folium
import matplotlib.pyplot as plt
from src.utils.constants import diccionario_aglomerados, PROJECT_PATH,PATHS
from src.functions_streamlit.empleo import *
from src.utils.loader import cargar_parcial_csv,cargar_json

st.title("Actividad y Empleo")

columnas_necesarias = ['AGLOMERADO','ANO4','TRIMESTRE', 'CONDICION_LABORAL', 'PP04A', 'PONDERA']
df = cargar_parcial_csv(PATHS["individual"]["csv"], usecols=columnas_necesarias)
fechas_disponibles = cargar_json(PATHS["individual"]["json"])

with open(PROJECT_PATH/'files' / "aglomerados_coordenadas.json", "r") as f:
    coordenadas_aglomerados =json.load(f)

# -------------------- 1.5.4 --------------------
st.header('Porcentaje de población ocupada por aglomerado')

nombres_aglomerados = list(diccionario_aglomerados.values())
nombre_seleccionado = st.selectbox("Seleccione un aglomerado", [""] + nombres_aglomerados)

def codigo_por_nombre(nombre):
    for codigo, nom in diccionario_aglomerados.items():
        if nom == nombre:
            return codigo
    return None

if nombre_seleccionado:
    codigo_seleccionado = codigo_por_nombre(nombre_seleccionado)

    # Calcula el porcentaje de ocupados y el desglose por tipo de empleo
    porcentaje_ocupados, labels, sizes = obtener_estadisticas_empleo(df, codigo_seleccionado)

    st.markdown(f"### Porcentaje de población ocupada en {nombre_seleccionado}: **{porcentaje_ocupados}%**")

    if sizes:
        # Genera el gráfico de torta
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        st.pyplot(fig)
    else:
        st.write("No hay datos de empleo para mostrar.")
else:
    st.write("Por favor, seleccione un aglomerado para visualizar los datos.")


# -------------------- 1.5.5 --------------------
st.header("Evolución de la tasa de empleo y desempleo")

tipo_tasa = st.selectbox("Seleccione qué desea visualizar:", ["Tasa de empleo", "Tasa de desempleo"])
# Calcula tasas de empleo y desempleo para cada aglomerado
tasas = calcular_tasas(df, fechas_disponibles)

# Inicializa el mapa centrado en Argentina
m = folium.Map(location=[-38, -64], zoom_start=4.5)

for aglomerado, valores in tasas.items():
    if aglomerado not in coordenadas_aglomerados:
        continue  # Saltea si no hay coordenadas para ese aglomerado

    coord = coordenadas_aglomerados[aglomerado]["coordenadas"]
    nombre = coordenadas_aglomerados[aglomerado]["nombre"]

    # Compara el valor actual con el antiguo según el tipo de tasa seleccionada
    if tipo_tasa == "Tasa de empleo":
        antiguo = valores["antiguo"]["empleo"]
        actual = valores["actual"]["empleo"]
        color = "green" if actual > antiguo else "red"
    else:
        antiguo = valores["antiguo"]["desempleo"]
        actual = valores["actual"]["desempleo"]
        color = "red" if actual > antiguo else "green"

    # Agrega cada aglomerado como marcador en el mapa
    popup_text = f"{nombre}<br>Antiguo: {antiguo}%<br>Actual: {actual}%"
    folium.CircleMarker(
        location=coord,
        radius=7,
        color=color,
        fill=True,
        fill_color=color,
        popup=popup_text
    ).add_to(m)

st_folium(m, width=700, height=500)
