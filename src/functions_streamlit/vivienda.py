"""Pagina 04. Funciones de análisis de vivienda"""
import sys
sys.path.append('..')
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

from src.utils.constants import diccionario_aglomerados


def filtrar_dataframe(df_viviendas, op):
    """
        recibe el Dataframe de viviendas y filtra según la opción 
        elegida. En caso de que un mismo CODUSU aparezca en varios
        años/trimestres, se queda con los datos más recientes, 
        excepto por la columna PONDERA, la cual promedia.
    """
    if(op != 'Mostrar para todos los años'):
        df_filtrado = df_viviendas[df_viviendas['ANO4']==op].copy()
    else:
        df_filtrado = df_viviendas.copy()

    # genero la columna PERIODO con el año y trimestre
    df_filtrado["PERIODO"] = df_filtrado["ANO4"].astype(str) + "T" + df_filtrado["TRIMESTRE"].astype(str)

    # Agrupo por CODUSU, quedandome con los datos más recientes para cada columna
    idx_ultimos = df_filtrado.groupby("CODUSU")["PERIODO"].idxmax()
    df_ultimos = df_filtrado.loc[idx_ultimos]

    # calculo el valor promedio de PONDERA para cada CODUSU
    ponderacion_promedio = df_filtrado.groupby('CODUSU',as_index=False)['PONDERA'].mean()

    # Reemplazo el valor más reciente de PONDERA con el valor promedio 
    # (elimino la columna anterior y hago un merge con la nueva)
    df_final = df_ultimos.drop(columns=["PONDERA"]).merge(ponderacion_promedio, on="CODUSU", how="left")

    # Transformo la columna PONDERA a valores enteros
    df_final["PONDERA"] = df_final["PONDERA"].fillna(0).astype(int)

    return df_final

# inciso 1
def hogares_encuestados(df_filtrado):
    """ Recibe el Dataframe filtrado por año e informa la cantidad total de 
        viviendas encuestadas"""
    total_encuestados = df_filtrado['PONDERA'].sum()
    st.write(f' - Cantidad de viviendas encuestados🏠: {total_encuestados:,}')


def categoria(tipo):
    """Recibe el tipo de vivienda y devuelve la representación
        en string acorde con el diseño de la EPH, Valores:
        1. casa
        2. departamento
        3. pieza de inquilinado
        4. pieza en hotel/pensión
        5. local no construido para habitación
        6. otro
        """
    match tipo:
          case 1:
                return 'Casa'
          case 2:
                return 'Departamento'
          case 3:
                return 'Pieza de inquilinato'
          case 4:
                return 'Pieza en hotel/pensión'
          case 5:
                return 'Local no construido para habitación'
          case 6: 
                return 'Otros'
          case _:
                return 'Indefinido' 

# inciso 2
def mostrar_grafico_torta(df_filtrado):
    """
        Recibe el Dataframe filtrado por año y genera un gráfico
        de torta con el porcentaje de cada tipo de vivienda
    """
    # valores del gráfico
    tipos_viviendas = df_filtrado.groupby('IV1')['PONDERA'].sum()      
    total_encuestados = df_filtrado['PONDERA'].sum()
    # etiquetas de los valores
    etiquetas = [f'{categoria(tipo)} ({(valor/total_encuestados):0.1%})' for tipo, valor in tipos_viviendas.items()]
    
    figura, ejex = plt.subplots(figsize=(5,3))
    
    # configuro el fondo transparente
    figura.patch.set_alpha(0)
    ejex.set_facecolor("none")

    # configuro colores del gráfico
    colores = [
    "#4363d8",
    "#e6194b", 
    "#3cb44b",
    "#ffe119", 
    "#f58231",
    "#911eb4", 
    ]

    ejex.pie(
        tipos_viviendas,
        autopct=None,
        labels=None,
        colors=colores
    )

    # leyenda con las etiquetas
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
    """
        recibe el valor correspondiente al tipo de piso
        y retorna su representación en string según el
        diseño de la EPH. Los valores son:
        1. Mosaico / baldosa / madera / cerámica / alfombra
        2. Cemento / ladrillo fijo
        3. Ladrillo suelto / tierra
        4. Otro
    """
    
    match int(tipo_piso):
        case 1:
                return 'Mosaico / baldosa / madera / cerámica / alfombra'
        case 2:
                return 'Cemento / ladrillo fijo'
        case 3:
            return 'Ladrillo suelto / tierra'
        case 4:
                return 'Otro'
        case _:
                return 'Sin información'
        
# inciso 3
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
    aglomerados_df['Aglomerado'] = aglomerados_df['AGLOMERADO'].astype(str).str.zfill(2).map(diccionario_aglomerados).fillna('-')
    aglomerados_df['Tipo de piso predominante'] = aglomerados_df['IV3'].apply(material_piso)  
    aglomerados_df.rename(columns={'AGLOMERADO' : 'Código'},inplace=True)

    # Asigno el nombre del aglomerado como índice
    aglomerados_df.set_index('Aglomerado',inplace=True)
    
    # borro columnas que no quiero mostrar
    aglomerados_df.drop(columns=['IV3','PONDERA'],inplace=True)
    
    # muestro el dataframe
    st.dataframe(aglomerados_df)


def mostrar_grafico_barras_horizontal(dict_viviendas):
    """
       Recibe el diccionario con la cantidad de viviendas 
       con baños interiores y cantidad total de viviendas
       por aglomerado y genera un gráfico de barras horizontal
       con los porcentajes
    """
    # alternativa : mostrar como dataframe 

    valores = []
    etiquetas = []
    for num, aglo in diccionario_aglomerados.items():
        if ((int(num) in dict_viviendas['banio_interior'])and(int(num) in dict_viviendas['totales'])):
            etiquetas.append(aglo)
            valores.append(dict_viviendas['banio_interior'][int(num)]*100 / dict_viviendas['totales'][int(num)])


    figura, ax = plt.subplots(figsize=(8, len(valores) * 0.3))

    y_pos = np.arange(len(etiquetas))
    colores = ["#4363d8","#e6194b", "#3cb44b", "#ffe119"]

    # saco el fondo
    figura.patch.set_alpha(0)
    ax.set_facecolor("none")

    # cambio el color de texto a blanco
    ax.tick_params(colors="white")
    ax.xaxis.label.set_color("white") 
    ax.title.set_color("white")

    ax.barh(y_pos, valores, color=colores)
    ax.set_yticks(range(len(etiquetas)))
    ax.set_yticklabels(etiquetas)
    ax.set_xlabel('Porcentaje')
    ax.set_title('Porcentaje de baños dentro de las viviendas por aglomerado')
    st.pyplot(figura)

# inciso 4
def mostrar_banios_por_aglomerado(df_filtrado):
    """"
        Recibe el dataframe filtrado por año y genera un gráfico
        de barras horizontal con el porcentaje de viviendas con baño
        interior por aglomerado
    """
    # armo el filtro con las columnas correspondientes
    tienen_banio_interior = (df_filtrado['IV8']==1)&(df_filtrado['IV9']==1)
    # genero dict con la cant de viviendas con baño interior y la cantidad de viviendas totales por aglomerado
    dict_viviendas = {
    'banio_interior' : df_filtrado[tienen_banio_interior].groupby('AGLOMERADO')['PONDERA'].sum().to_dict(),
    'totales' : df_filtrado.groupby('AGLOMERADO')['PONDERA'].sum().to_dict()
    }

    mostrar_grafico_barras_horizontal(dict_viviendas)


def obtener_regimen_str(num):
    """
        Recibe el valor correspondiente al régimen de la vivienda
        y devuelve la representación en string acorde el diseño
        de la EPH. Los valores son:
        1. 'Propietario vivienda y terreno'
        2. 'Propietario vivienda'
        3. 'Inquilino'
        4. 'Ocupante por impuestos / expensas'
        5. 'Ocupante por dependencia'
        6. 'Ocupante gratuito'
        7. 'Ocupante de hecho'
        8. 'En sucesión'
        9. 'Otro'
    """
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
        case _:
            return 'Otro'

# inciso 5
def evolucion_regimen(anio,aglomerado_elegido,df_viviendas):
    """
        Recibe el año y aglomerado seleccionados por el usuario
        y el dataframe de viviendas.
        Genera un gráfico de líneas con la evolución de los regímenes
        de las viviendas durante los trimestres para ese año y aglomerado.
        En caso de no haber información, lo informa.
    """

    # filtro por año si corresponde
    if(anio != 'Mostrar para todos los años'):
        df_filtrado = df_viviendas[df_viviendas['ANO4']==anio]
    else:
        df_filtrado = df_viviendas

    # obtengo el nombre del aglomerado de cada fila para poder filtrar
    aglomerados_filas = df_filtrado['AGLOMERADO'].astype(str).str.zfill(2).map(diccionario_aglomerados)
    
    # filtro por aglomerado y chequeando que el valor del régimen sea válido
    df_aglomerado_elegido = df_filtrado[
        (aglomerados_filas==aglomerado_elegido)&
        (df_filtrado['II7'].isin(range(1,10)))
        ].copy() 

    # si el dataframe está vacío, no lo proceso
    if(df_aglomerado_elegido.empty):
         st.warning('No hay datos para el aglomerado en el año elegido')
         return

    # agrupo por año, trimestre y tipo de régimen
    df_por_regimen = df_aglomerado_elegido.groupby(['ANO4','TRIMESTRE','II7'])['PONDERA'].sum().reset_index()
    
    # genero para cada tipo de régimen, una columna con la cantidad de viviendas con ese régimen
    for i in range (0,10):
        df_por_regimen[obtener_regimen_str(i)] = (df_por_regimen['II7']==i)*df_por_regimen['PONDERA']

    # genero columna PERIODO con la información de año y trimestre 
    df_por_regimen["PERIODO"] = df_por_regimen["ANO4"].astype(str) + "T" + df_por_regimen["TRIMESTRE"].astype(str)

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

    # widget para elegir que regímenes mostrar
    opciones = st.multiselect(
        'Elegir categorías:',
        options=df_por_regimen.columns.tolist(),
        default=df_por_regimen.columns.tolist()[:2]  # por defecto se muestran las 2 primeras opciones
    )
    if opciones:
        # genero el gráfico
        st.line_chart(df_por_regimen[opciones])
    else:
        st.warning('Seleccione al menos una variable para mostrar el gráfico.')
        
# inciso 6
def viviendas_en_villa_por_aglomerado(df):
    """
    Calcula la cantidad y el porcentaje de viviendas ubicadas en villas de emergencia por aglomerado.

    Args:
        df (pd.DataFrame): DataFrame con los datos de viviendas, incluyendo las columnas 'AGLOMERADO',
                           'IV12_3' (ubicación en villa) y 'PONDERA' (ponderación).

    Returns:
        pd.DataFrame: DataFrame ordenado de forma decreciente por cantidad de viviendas en villa.
                      Incluye las columnas 'Aglomerado', 'Cantidad' (ponderada) y 'Porcentaje' respecto del total.
    """
    df = df.copy()
    df['AGLOMERADO'] = df['AGLOMERADO'].astype(str).str.zfill(2)
    
    #Total de viviendas por aglomerado
    total_por_aglo = df.groupby('AGLOMERADO')['PONDERA'].sum()
    
    en_villa = df[df['IV12_3'] == 1].groupby('AGLOMERADO')['PONDERA'].sum()
      
    #Se une todo en un DataFrame
    resumen = pd.DataFrame({'Cantidad': en_villa,'Total': total_por_aglo}).fillna(0)

    resumen['Porcentaje'] = (resumen['Cantidad'] / resumen['Total'] * 100).round(2)

    # Agregar nombre del aglomerado
    resumen = resumen.reset_index()
    resumen['Aglomerado'] = resumen['AGLOMERADO'].map(diccionario_aglomerados)

    # Reordenar columnas y ordenar
    resumen = resumen[['Aglomerado', 'Cantidad', 'Porcentaje']]
    return resumen.sort_values(by='Cantidad', ascending=False)

# inciso 7
def porcentaje_viviendas_por_condicion(df):
    """
    Calcula el porcentaje de viviendas por condición de habitabilidad para cada aglomerado.

    Args:
        df (pd.DataFrame): DataFrame con los datos de viviendas, incluyendo columnas 'AGLOMERADO',
                           'CONDICION_DE_HABITABILIDAD' y 'PONDERA'.

    Returns:
        pd.DataFrame: DataFrame con una fila por aglomerado y una columna para cada condición de habitabilidad,
                      con los porcentajes correspondientes.
    """
    df = df.copy()
    df['AGLOMERADO'] = df['AGLOMERADO'].astype(str).str.zfill(2)

    # Agrupamos por aglomerado y condición de habitabilidad
    tabla = df.groupby(['AGLOMERADO', 'CONDICION_DE_HABITABILIDAD'])['PONDERA'].sum().unstack(fill_value=0)

    # Calculamos totales por aglomerado
    tabla['TOTAL'] = tabla.sum(axis=1)

    # Calculamos porcentajes por cada condición
    for col in tabla.columns[:-1]:  # omitimos la columna TOTAL
        tabla[col] = (tabla[col] / tabla['TOTAL'] * 100).round(2)

    tabla = tabla.drop(columns='TOTAL').reset_index()

    # Reemplazar códigos por nombres de aglomerados
    tabla['Aglomerado'] = tabla['AGLOMERADO'].map(diccionario_aglomerados)

    # Reordenar columnas
    columnas = ['Aglomerado'] + [col for col in tabla.columns if col not in ['Aglomerado', 'AGLOMERADO']]
    return tabla[columnas].sort_values(by='Aglomerado')