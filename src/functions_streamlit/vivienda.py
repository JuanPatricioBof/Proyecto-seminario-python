"""Pagina 04. Funciones de análisis de vivienda"""
import sys
import os
sys.path.append('..')
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

from src.utils.constants import diccionario_aglomerados

def filtrar_dataframe(df_viviendas, op):
        
    if(op != 'Mostrar para todos los años'):
        df_filtrado = df_viviendas[df_viviendas['ANO4']==op]
    else:
        df_filtrado = df_viviendas

    # genero la columna PERIODO con el año y trimestre
    df_filtrado["PERIODO"] = df_filtrado["ANO4"].astype(str) + "T" + df_filtrado["TRIMESTRE"].astype(str)

    # Agrupo por CODUSU, quedandome con los datos más recientes para cada columna
    idx_ultimos = df_filtrado.groupby("CODUSU")["PERIODO"].idxmax()
    df_ultimos = df_filtrado.loc[idx_ultimos]

    # calculo el valor promedio de PONDERA para cada CODUSU
    ponderacion_promedio = df_filtrado.groupby('CODUSU',as_index=False)['PONDERA'].mean()

    # Reemplazo el valor más reciente de PONDERA con el valor promedio
    df_final = df_ultimos.drop(columns=["PONDERA"]).merge(ponderacion_promedio, on="CODUSU", how="left")

    # Transformo la columna PONDERA a valores enteros
    df_final["PONDERA"] = df_final["PONDERA"].fillna(0).astype(int)

    st.dataframe(df_final.head(30))

    return df_final




def hogares_encuestados(df_filtrado):
    viviendas = df_filtrado.groupby(['CODUSU'])['PONDERA'].mean()
    total_encuestados = int(viviendas.sum())
    st.write(f' - Cantidad de hogares encuestados🏠: {total_encuestados:,}')


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


def mostrar_grafico_torta(df_filtrado):
    
    tipos_viviendas = df_filtrado.groupby('IV1')['PONDERA'].sum()      
    total_encuestados = df_filtrado['PONDERA'].sum()
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


def material_piso(tipo_piso):
    match int(tipo_piso):
        case 1:
                return 'mosaico / baldosa / madera / cerámica / alfombra'
        case 2:
                return 'cemento / ladrillo fijo'
        case 3:
            return 'ladrillo suelto / tierra'
        case 4:
                return 'otro'
        case _:
                return 'sin información'
        

def mostrar_piso_dominante(fila):
    num_aglo = str(fila['AGLOMERADO']).zfill(2)
    tipo_piso = int(fila['IV3'])
    if(num_aglo in diccionario_aglomerados):
        st.write(f'{diccionario_aglomerados[num_aglo]}({num_aglo}): {material_piso(tipo_piso)}')
    else:
        st.warning(f'no se encontró el aglomerado {num_aglo}. Omitido')



def informar_piso_dominante_por_aglomerado(df_filtrado):
    """
        Recibe el dataframe filtrado por año y muestra para cada aglomerado
        el tipo de piso interior dominante en formato dataframe (En caso de
        que no haya datos disponibles lo avisa).
    """  
        
    # agrupo por aglomerado y por tipo de piso, cuento la cant de hogares
    pisos_por_aglo = df_filtrado.groupby(['AGLOMERADO','IV3'])['PONDERA'].sum()

    # reseteo el indice para poder trabajar con el aglomerado y piso como valores, ordeno por columna PONDERA
    df_tipo_piso = pisos_por_aglo.reset_index().sort_values(by=['PONDERA'],ascending=False)

    # filtro los aglomerados repetidos para quedarme solo con el piso dominante
    df_piso_dominante = df_tipo_piso.drop_duplicates(subset='AGLOMERADO',keep='first')

    # lista de aglomerados que están en el dataframe:
    aglomerados_df = [aglo.zfill(2) for aglo in df_piso_dominante['AGLOMERADO'].unique().astype(str)]

    # genero las filas con los aglomerados que faltan
    nuevas_filas = pd.DataFrame([
            {'AGLOMERADO': aglo, 'IV3': 0, 'PONDERA': 0} 
            for num, aglo in diccionario_aglomerados.items()
            if not num in aglomerados_df
         ])
    
    # añado las nuevas filas al dataframe
    aglomerados_df = pd.concat([df_piso_dominante,nuevas_filas], ignore_index=True)

    # Genero y renombro columnas para la visualización de la información
    aglomerados_df['Aglomerado'] = aglomerados_df['AGLOMERADO'].astype(str).str.zfill(2).map(diccionario_aglomerados)
    aglomerados_df['Tipo de piso predominante'] = aglomerados_df['IV3'].apply(material_piso)  
    aglomerados_df.rename(columns={'AGLOMERADO' : 'Código'},inplace=True)

    # Asigno el nombre del aglomerado como índice
    aglomerados_df.set_index('Aglomerado',inplace=True)
    
    # borro columnas que no quiero mostrar
    aglomerados_df.drop(columns=['IV3','PONDERA'],inplace=True)
    
    # muestro el dataframe
    st.dataframe(aglomerados_df)


def mostrar_banios_por_aglomerado(df_filtrado):
     # total_banios = 
    #st.write(banio_dentro_vivienda)
    #st.write(total_encuestados_aglomerado)
    #df_merged = banio_dentro_vivienda.merge(total_encuestados_aglomerado,how='right',left_index=True,right_index=True)
    #st.dataframe(df_merged)

    # genero dict con la cant de viviendas con baño interior y la cantidad de viviendas totales por aglomerado
    dict_viviendas = {
    'banio_interior' : df_filtrado[(df_filtrado['IV8']==1)&(df_filtrado['IV9']==1)].groupby('AGLOMERADO')['PONDERA'].sum().to_dict(),
    'totales' : df_filtrado.groupby('AGLOMERADO')['PONDERA'].sum().to_dict()
    }

    mostrar_grafico_barras(dict_viviendas)


def mostrar_grafico_barras(dict_viviendas):
    
    # alternativa : mostrar como dataframe 

    valores = []
    etiquetas = []
    for num, aglo in diccionario_aglomerados.items():
        if ((int(num) in dict_viviendas['banio_interior'])and(int(num) in dict_viviendas['totales'])):
            etiquetas.append(aglo)
            valores.append(dict_viviendas['banio_interior'][int(num)]*100 / dict_viviendas['totales'][int(num)])


    figura, ax = plt.subplots(figsize=(8, len(valores) * 0.3))

    y_pos = np.arange(len(etiquetas))
    #error = np.random.rand(len(etiquetas))

    ax.barh(y_pos, valores)
    ax.set_yticks(range(len(etiquetas)))
    ax.set_yticklabels(etiquetas)
    ax.set_xlabel('Porcentaje')
    ax.set_title('Porcentaje de baños dentro de las viviendas por aglomerado')
    st.pyplot(figura)


def obtener_valor(coincidencia,ponderacion):
    if coincidencia:
        return ponderacion
    else:
        return 0


def obtener_periodo(anio, trimestre):
    return str(anio) + 'T' + str(trimestre)


def obtener_regimen(num):
    match int(num):
        case 1:
            return 'Propietario vivienda y terreno'
        case 2:
            return 'Propietario vivienda'
        case 3:
            return 'Inquilino'
        case 4:
            return 'Ocupante por impuestos / expensas'
        case 5:
            return 'Ocupante por dependencia'
        case 6:
            return 'Ocupante gratuito'
        case 7:
            return 'Ocupante de hecho'
        case 8:
            return 'En sucesión'
        case 9:
              return 'Otro'
        case _:
            return 'Indefinido'

# eliminar ?
def calcular_porcentaje(valor,total):
    return int(valor)*100 / int(total)


def evolucion_regimen(anio,aglomerado_elegido,df_viviendas):
    
    # filtro por año 
    if(anio != 'Mostrar para todos los años'):
        df_filtrado = df_viviendas[df_viviendas['ANO4']==anio]
    else:
        df_filtrado = df_viviendas

    # obtengo el nombre del aglomerado de cada fila para poder filtrar
    aglomerados_filas = df_filtrado['AGLOMERADO'].astype(str).str.zfill(2).map(diccionario_aglomerados)
    
    # filtro por aglomerado
    df_aglomerado_elegido = df_filtrado[
        (aglomerados_filas==aglomerado_elegido)&
        (df_filtrado['II7'].isin(range(1,10)))
        ].copy() 

    # si está vacío, no lo proceso
    if(df_aglomerado_elegido.empty):
         st.warning('No hay datos para el aglomerado elegido')
         return

    # agrupo por año, trimestre y tipo de régimen
    df_por_regimen = df_aglomerado_elegido.groupby(['ANO4','TRIMESTRE','II7'])['PONDERA'].sum().reset_index()
    
    # genero para cada tipo de régimen, una columna con la cantidad de viviendas con ese régimen
    for i in range (0,10):
        df_por_regimen[obtener_regimen(i)] = (df_por_regimen['II7']==i)*df_por_regimen['PONDERA']

    # genero columna PERIODO con la información de año y trimestre 
    df_por_regimen['PERIODO'] = df_por_regimen.apply(
        lambda x: obtener_periodo(x['ANO4'],x['TRIMESTRE']),axis=1
        )

    # actualizo el indice
    df_por_regimen.set_index('PERIODO',inplace=True)

    # elimino las columnas que ya usé
    df_por_regimen.drop(columns=['ANO4','TRIMESTRE','II7'], inplace = True)

    # agrupo por PERIODO sumando las columnas 
    df_por_regimen = df_por_regimen.groupby(['PERIODO']).sum()

    # ahora para cada fila tengo la cantidad total de viviendas en ese periodo (PONDERA), y la cantidad
    # de viviendas para cada regimen en su respectiva columna

    # para fila, calculo el porcentaje de todas las columnas
    df_por_regimen = df_por_regimen.apply((lambda x : (x*100)/df_por_regimen['PONDERA'])).drop('PONDERA',axis=1)

    # armar grafico
    # ver si sacar 'indefinido' o dejarla
    opciones = st.multiselect(
        'Elegir categorías:',
        options=df_por_regimen.columns.tolist(),
        default=df_por_regimen.columns.tolist()[:2]  # por defecto se muestran las 2 primeras
    )
    if opciones:
        st.line_chart(df_por_regimen[opciones])
    else:
        st.warning('Seleccione al menos una variable para mostrar el gráfico.')
        

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
