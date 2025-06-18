import sys
import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Agrega "code/src" al sys.path
sys.path.append('..')

from src.utils.constants import PATHS
from src.utils.loader import cargar_parcial_csv, cargar_json
from src.functions_streamlit.vivienda import hogares_encuestados
from src.functions_streamlit.vivienda import mostrar_grafico_torta


# carga de dataframe
columnas=['ANO4','TRIMESTRE','AGLOMERADO','PONDERA','IV1','IV1_ESP','IV3','IV3_ESP',
            'IV8','IV9','IV12_3','II7','II7_ESP','CONDICION_DE_HABITABILIDAD'] 

#df_viviendas = cargar_parcial_csv(PATHS['hogar']['csv'],columnas)
#json_fechas = cargar_json(PATHS['hogar'['json']])

df_viviendas = pd.read_csv(PATHS['hogar']['csv'],sep=';',usecols=columnas)
json_fechas = pd.read_json(PATHS['hogar']['json'])

# lista de años
opciones = [anio for anio in json_fechas]
opciones.append('Mostrar para todos los años')

# Interfaz 
st.title("Características de la vivienda.")

# filtrado (modularizar?)

op = st.selectbox("Elegir año",opciones,index=len(opciones)-1,key='anio_p3')
if(op != 'Mostrar para todos los años'):
    df_filtrado = df_viviendas[df_viviendas['ANO4']==op]
else:
   df_filtrado = df_viviendas

# Inciso 1
total_encuestados = hogares_encuestados(df_filtrado['PONDERA'])
st.write(f' - Cantidad de hogares encuestados🏠: {total_encuestados}')

# Inciso 2
st.subheader('Distribución según tipos de hogar en Argentina')
mostrar_grafico_torta(df_filtrado,total_encuestados)

# Inciso 3
#informar_piso_dominante_por_aglomerado(df_filtrado)

# Inciso 4

# Inciso 5
