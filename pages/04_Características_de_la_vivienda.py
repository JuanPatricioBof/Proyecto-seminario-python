import sys
import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Agrega "code/src" al sys.path
sys.path.append('..')

from src.utils.constants import PATHS, diccionario_aglomerados
from src.utils.loader import cargar_parcial_csv, cargar_json
from src.functions_streamlit.vivienda import hogares_encuestados, mostrar_banios_por_aglomerado, evolucion_regimen
from src.functions_streamlit.vivienda import mostrar_grafico_torta, informar_piso_dominante_por_aglomerado, filtrar_dataframe
from src.functions_streamlit.vivienda import viviendas_en_villa_por_aglomerado, porcentaje_viviendas_por_condicion


# carga de dataframe
columnas=['CODUSU','ANO4','TRIMESTRE','AGLOMERADO','PONDERA','IV1','IV3',
            'IV8','IV9','IV12_3','II7','CONDICION_DE_HABITABILIDAD'] 

df_viviendas = cargar_parcial_csv(PATHS['hogar']['csv'],columnas)
json_fechas = cargar_json(PATHS['hogar']['json'])

# lista de años
opciones = [anio for anio in json_fechas]
opciones.append('Mostrar para todos los años')

# Interfaz 
st.title("Características de la vivienda.")

# filtrado del dataframe
op = st.selectbox("Años disponibles",opciones,index=len(opciones)-1)
if(op):
    df_filtrado = filtrar_dataframe(df_viviendas,op)


# Inciso 1 : Mostrar total de viviendas encuestadas
hogares_encuestados(df_filtrado)

# Inciso 2 : Mostrar porcentaje de tipos de vivienda
st.subheader('Distribución de tipos de vivienda en Argentina')
mostrar_grafico_torta(df_filtrado)

# Inciso 3 : Mostrar piso interior predominante por aglomerado
st.subheader('📍 Piso predominante en el interior de las viviendas por aglomerado')
informar_piso_dominante_por_aglomerado(df_filtrado)

# Inciso 4 : mostrar % de baños interiores por aglomerado
mostrar_banios_por_aglomerado(df_filtrado)

# Inciso 5 : mostrar evolución de régimen de tenencia para un aglomerado elegido
st.subheader('Evolución de régimen de tenencia')

aglomerado_elegido = st.selectbox(
    'Elija un aglomerado para ver su evolución de régimen de tenencias',
    options=diccionario_aglomerados.values() # mejorar
)

evolucion_regimen(op,aglomerado_elegido,df_viviendas)


#Inciso 6
st.subheader("1.4.6 cantidad de viviendas ubicadas en villa de emergencia por aglomerado")
resumen = viviendas_en_villa_por_aglomerado(df_filtrado, diccionario_aglomerados)
st.dataframe(
    resumen.style.format({
        'Cantidad': '{:,.0f}',
        'Porcentaje': '{:.2f}%'
    }).hide(axis="index"),
    use_container_width=True,
    height=min(500, 35 * len(resumen) + 35)
)

#Inciso 7
tabla_resultado = porcentaje_viviendas_por_condicion(df_viviendas, diccionario_aglomerados, op)

st.dataframe(tabla_resultado, use_container_width=True)

# Exportar CSV
csv = tabla_resultado.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Descargar CSV",
    data=csv,
    file_name=f"porcentaje_viviendas_condicion_{op}.csv",
    mime="text/csv"
)
