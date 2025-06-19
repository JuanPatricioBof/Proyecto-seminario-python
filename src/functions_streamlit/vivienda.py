"""Pagina 04. Funciones de análisis de vivienda"""
import sys
import os
sys.path.append('..')
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

from src.utils.constants import diccionario_aglomerados

def hogares_encuestados(df_filtrado):
        return df_filtrado['PONDERA'].sum()


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
                return 'indefinido'
        

def mostrar_piso_dominante(fila):
    num_aglo = str(fila['AGLOMERADO']).zfill(2)
    tipo_piso = int(fila['IV3'])
    if(num_aglo in diccionario_aglomerados):
        st.write(f'{diccionario_aglomerados[num_aglo]}({num_aglo}): {material_piso(tipo_piso)}')
    else:
        st.warning(f'no se encontró el aglomerado {num_aglo}. Omitido')


def informar_piso_dominante_por_aglomerado(df_filtrado):
    # alternativa para mostrar: usar st.dataframe (permite descargar como csv, entre otros)  
    """
    Los pisos interiores son principalmente
    de...   
    1. mosaico / baldosa / madera /
    cerámica / alfombra
    2. cemento / ladrillo fijo
    3. ladrillo suelto / tierra
    4. otro
    """  
        
    # agrupo por aglomerado y por tipo de piso, cuento la cant de hogares
    pisos = df_filtrado.groupby(['AGLOMERADO','IV3'])['PONDERA'].sum()

    # reseteo el indice para poder trabajar con el aglomerado y piso como valores, ordeno por columna pondera
    piso2 = pisos.reset_index().sort_values(by=['PONDERA'],ascending=False)

    # filtro los aglomerados repetidos para quedarme solo con el piso dominante
    pisos3 = piso2.drop_duplicates(subset='AGLOMERADO',keep='first')

    # muestro la informacion
    pisos3.apply(mostrar_piso_dominante, axis=1)

    # aglomerados que si estan en el dataset:
    aglomerados = [aglo.zfill(2) for aglo in pisos3['AGLOMERADO'].unique().astype(str)]

    # muestro aglomerados que no están en el dataset
    for num, aglo in diccionario_aglomerados.items():
        if not num in aglomerados:
            st.write(f'{aglo}({num}): sin información')


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


diccionario_aglomerados_inv={
    'Gran La Plata' : '02',
    'Bahía Blanca - Cerri': '03' ,
    'Gran Rosario' : '04',
    'Gran Santa Fé' : '05',
    'Gran Paraná' : '06',
    'Posadas' : '07',
    'Gran Resistencia' : '08',
    'Comodoro Rivadavia - Rada Tilly' : '09',
    'Gran Mendoza' : '10',
    'Corrientes' : '12',
    'Gran Córdoba' : '13',
    'Concordia' : '14',
    'Formosa' : '15',
    'Neuquén - Plottier' : '17',
    'Santiago del Estero - La Banda' : '18',
    'Jujuy - Palpalá' : '19',
    'Río Gallegos' : '20',
    'Gran Catamarca' : '22',
    'Gran Salta' : '23',
    'La Rioja' : '25',
    'Gran San Luis' : '26',
    'Gran San Juan' : '27',
    'Gran Tucumán - Tafí Viejo' : '29',
    'Santa Rosa - Toay' : '30',
    'Ushuaia - Río Grande' : '31',
    'Ciudad Autónoma de Buenos Aires' : '32',
    'Partidos del GBA' : '33',
    'Mar del Plata' : '34',
    'Río Cuarto' : '36',
    'San Nicolás - Villa Constitución' : '38',
    'Rawson - Trelew' : '91',
    'Viedma- Carmen de Patagones' : '93',
    }


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


def evolucion_regimen(aglomerado_elegido,df_filtrado):
    # filtrar por aglomerado
    df_aglomerado_elegido = df_filtrado[
        df_filtrado['AGLOMERADO']== int(diccionario_aglomerados_inv[aglomerado_elegido])
        ].copy() 

    # si df vacio, no procesar !!

    #agrupar por año, trimestre y tipo
    df_por_regimen = df_aglomerado_elegido.groupby(['ANO4','TRIMESTRE','II7'])['PONDERA'].sum().reset_index()
    # chequeo
    #st.dataframe(df_por_regimen)

    # genero para cada tipo de regimen, una nueva columna   
    for i in range (0,10):
        df_por_regimen[obtener_regimen(i)] = df_por_regimen.apply(
            lambda x: obtener_valor(int(x['II7'])==i, x['PONDERA']), axis=1
            )

    # genero columna periodo 
    df_por_regimen['PERIODO'] = df_por_regimen.apply(
        lambda x: obtener_periodo(x['ANO4'],x['TRIMESTRE']),axis=1
        )

    # actualizo el indice
    df_por_regimen.set_index('PERIODO',inplace=True)
    # chequeo
    #st.dataframe(df_por_regimen)

    # elimino columnas, agrupo por periodo y sumo las ponderaciones
    df_por_regimen = df_por_regimen.drop(columns=['ANO4','TRIMESTRE','II7']).groupby(['PERIODO']).sum()

    # aplico la operacion para calcular el porcentaje
    df_por_regimen = df_por_regimen.apply((lambda x : (x*100)/df_por_regimen['PONDERA'])).drop('PONDERA',axis=1)
    # chequeo
    #st.dataframe(df_por_regimen)

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

