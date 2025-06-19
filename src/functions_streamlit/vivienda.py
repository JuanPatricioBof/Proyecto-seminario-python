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

def viviendas_en_villa_por_aglomerado(df, diccionario_aglomerados):
    """
    Devuelve cantidad y porcentaje de viviendas en villa por aglomerado (nombre),
    ordenado de forma decreciente por cantidad.
    """
    df = df[df['IV12_3'].isin([1, 2])].copy()

    total_por_aglo = df.groupby('AGLOMERADO').size()
    en_villa = df[df['IV12_3'] == 1].groupby('AGLOMERADO').size()

    resumen = pd.DataFrame({
        'Cantidad': en_villa,
        'Total': total_por_aglo
    }).fillna(0)

    resumen['Cantidad'] = resumen['Cantidad'].astype(int)
    resumen['Porcentaje'] = (resumen['Cantidad'] / resumen['Total'] * 100).round(2)

    # Agregar nombre del aglomerado
    resumen = resumen.reset_index()
    resumen['AGLOMERADO'] = resumen['AGLOMERADO'].astype(str).str.zfill(2)
    resumen['Aglomerado'] = resumen['AGLOMERADO'].map(diccionario_aglomerados)

    # Reordenar columnas y ordenar
    resumen = resumen[['Aglomerado', 'Cantidad', 'Porcentaje']]
    return resumen.sort_values(by='Cantidad', ascending=False)

def porcentaje_viviendas_por_condicion(df, diccionario_aglomerados, ano):
    df = df.copy()
    df['AGLOMERADO'] = df['AGLOMERADO'].astype(str).str.zfill(2)

    # Filtrar por año seleccionado
    df = df[df['ANO4'] == ano]

    # Agrupamos por aglomerado y condición de habitabilidad
    tabla = df.groupby(['AGLOMERADO', 'CONDICION_DE_HABITABILIDAD']).size().unstack(fill_value=0)

    # Calculamos totales por aglomerado
    tabla['TOTAL'] = tabla.sum(axis=1)

    # Calculamos porcentajes por cada condición
    for col in tabla.columns[:-1]:  # omitimos TOTAL
        tabla[col] = (tabla[col] / tabla['TOTAL'] * 100).round(2)

    tabla = tabla.drop(columns='TOTAL').reset_index()

    # Reemplazar códigos por nombres de aglomerados
    tabla['Aglomerado'] = tabla['AGLOMERADO'].map(diccionario_aglomerados)

    # Reordenar columnas
    columnas = ['Aglomerado'] + [col for col in tabla.columns if col not in ['Aglomerado', 'AGLOMERADO']]
    return tabla[columnas].sort_values(by='Aglomerado')
