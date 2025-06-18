"""Pagina 04. Funciones de análisis de vivienda"""
import sys
import os
sys.path.append('..')
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

from src.utils.constants import diccionario_aglomerados

def hogares_encuestados(ponderacion_hogares):
        return ponderacion_hogares.sum()

def categoria(tipo):
    #1. casa
    #2. departamento
    #3. pieza de inquilinato
    #4. pieza en hotel / pensión
    #5. local no construido para habitación
    match int(tipo):
          case 1:
                return 'casa'
          case 2:
                return 'departamento'
          case 3:
                return 'pieza de inquilinato'
          case 4:
                return 'pieza en hotel/pensión'
          case 5:
                return 'local no construido para habitación'
          case 6: 
                return 'otros'
          case _:
                return 'indefinido' 

def mostrar_grafico_torta(df_filtrado, total_encuestados):
    
    tipos_viviendas = df_filtrado.groupby('IV1')['PONDERA'].sum()      
    
    etiquetas = [f'{categoria(tipo)} ({(valor/total_encuestados):0.1%})' for tipo, valor in tipos_viviendas.items()]
    
    figura, ejex = plt.subplots(figsize=(5,3))
    
    ejex.pie(
        tipos_viviendas,
        autopct=None,
        labels=None
    )

    ejex.legend(
        title = 'Tipo de vivienda',
        labels = etiquetas,
        bbox_to_anchor=(1, 0.5), 
        loc="center left"
    )

    ejex.set_ylabel('')
    ejex.set_title='Distribución de tipo de viviendas en Argentina'

    st.pyplot(figura)

def informar_piso_dominante_por_aglomerado(df_filtrado):
      df_filtrado.groupby(['AGLOMERADO','IV3'])['PONDERA'].sum()



