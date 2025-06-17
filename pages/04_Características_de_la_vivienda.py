import sys
import os

# Agrega "code/src" al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from utils.constants import PATHS
import streamlit as st
import pandas as pd


# carga de dataframe
columnas=['ANO4','TRIMESTRE','AGLOMERADO','PONDERA','IV1','IV1_ESP','IV3','IV3_ESP',
            'IV8','IV9','IV12_3','II7','II7_ESP','CONDICION_DE_HABITABILIDAD'] 

df_viviendas = cargar_parcial_csv(PATHS['hogar']['csv'],columnas)
json_fechas = cargar_json(PATHS['hogar'['json']])

# seleccionar un año
opciones = [anio for anio in json_fechas]
opciones.append('Mostrar para todos los años')

# Interfaz 
st.title("Características de la vivienda.")
op = st.selectbox("Elegir año",opciones,index=len(opciones)-1)

# filtrado 
if(op != 'Mostrar para todos los años'):
   df_filtrado = df_viviendas[df_viviendas['ANO4']==op]
else:
   df_filtrado = df_viviendas

