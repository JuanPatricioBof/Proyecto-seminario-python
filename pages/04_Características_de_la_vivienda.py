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
from src.functions_streamlit.vivienda import mostrar_grafico_torta, informar_piso_dominante_por_aglomerado
from src.functions_streamlit.vivienda import viviendas_en_villa_por_aglomerado, porcentaje_viviendas_por_condicion


# carga de dataframe
columnas=['ANO4','TRIMESTRE','AGLOMERADO','PONDERA','IV1','IV1_ESP','IV3','IV3_ESP',
            'IV8','IV9','IV12_3','II7','II7_ESP','CONDICION_DE_HABITABILIDAD'] 

df_viviendas = cargar_parcial_csv(PATHS['hogar']['csv'],columnas)
json_fechas = cargar_json(PATHS['hogar']['json'])

#df_viviendas = pd.read_csv(PATHS['hogar']['csv'],sep=';',usecols=columnas)
#json_fechas = pd.read_json(PATHS['hogar']['json'])

# lista de años
opciones = [anio for anio in json_fechas]
opciones.append('Mostrar para todos los años')

# Interfaz 
st.title("Características de la vivienda.")

# filtrado (modularizar?)

op = st.selectbox("Elegir año",opciones,index=len(opciones)-1)
if(op != 'Mostrar para todos los años'):
    df_filtrado = df_viviendas[df_viviendas['ANO4']==op]
else:
   df_filtrado = df_viviendas

# Inciso 1
total_encuestados = hogares_encuestados(df_filtrado)
st.write(f' - Cantidad de hogares encuestados🏠: {total_encuestados:,}')

# Inciso 2
st.subheader('Distribución de tipos de hogar en Argentina')
mostrar_grafico_torta(df_filtrado,total_encuestados)

# Inciso 3
with st.expander('Piso predominante en el interior de las viviendas por aglomerado',icon='📍'):
    informar_piso_dominante_por_aglomerado(df_filtrado)

# Inciso 4
mostrar_banios_por_aglomerado(df_filtrado)

# Inciso 5

st.subheader('Evolución de régimen de tenencia')


aglomerado_elegido = st.selectbox(
    'Elija un aglomerado para ver su evoolución de régimen de tenencias',
    options=diccionario_aglomerados.values() # mejorar
)

evolucion_regimen(aglomerado_elegido,df_filtrado)


#Inciso 6
st.subheader("Cantidad de viviendas ubicadas en villa de emergencia por aglomerado")
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
st.subheader("Porcentaje de vivendas para cada condicion de habitabilidad")
tabla_resultado = porcentaje_viviendas_por_condicion(df_filtrado, diccionario_aglomerados)

st.dataframe(tabla_resultado, use_container_width=True)

# Exportar CSV
csv = tabla_resultado.to_csv(index=False).encode('utf-8')
st.download_button(label="📥 Descargar CSV",data=csv,file_name=f"porcentaje_viviendas_condicion_{op}.csv",mime="text/csv")