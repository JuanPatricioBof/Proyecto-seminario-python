import pandas as pd
def calcular_trimestre(mes):
    """Calcula el trimestre a partir del mes dado"""
    if mes in [1, 2, 3]:
        return 1
    elif mes in [4, 5, 6]:
        return 2
    elif mes in [7, 8, 9]:
        return 3
    elif mes in [10, 11, 12]:
        return 4
    else:
        raise ValueError("Mes inválido. Debe ser un número entre 1 y 12.")
    

def procesar_canasta(df_canasta):
    """Procesa el DataFrame de la canasta basica y devuelve un dataframe con un valor trimestral"""
    #se crea una copia 
    df_canasta=df_canasta.copy()
    #Se convierte el indice de tiempo a fecha
    df_canasta['indice_tiempo'] = pd.to_datetime(df_canasta['indice_tiempo'])
    df_canasta['ANIO']=df_canasta['indice_tiempo'].dt.year
    df_canasta['MES']=df_canasta['indice_tiempo'].dt.month
    df_canasta['TRIMESTRE'] = df_canasta['MES'].apply(calcular_trimestre)
    
    #Asignamos CBT y CBI  a partir de las columnas del csv de canasta basica
    df_canasta['CBT'] = df_canasta['canasta_basica_total']
    df_canasta['CBI'] = df_canasta['canasta_basica_alimentaria']

    #Calculamos el promedio trimestral
    canasta_promedio = df_canasta.groupby(['ANIO', 'TRIMESTRE'], ).agg({
        'CBT': 'mean',
        'CBI': 'mean'
    }).reset_index()

    return canasta_promedio

def filtrar_hogares(df, anio, trimestre):
    """Filtra los hogares que contengan 4 integrantes a partir de un anio y trimestre dados"""
    hogares_4_integrantes = df[df['IX_TOT']==4 ]
    filtro=hogares_4_integrantes[(hogares_4_integrantes['ANO4']==anio) & (hogares_4_integrantes['TRIMESTRE']==trimestre)]
    return filtro

def calcular_ingresos(df, cbt, cbi):
    """Calcula los ingresos de los hogares filtrados y devuelve un diccionario con las estadísticas a imprimir en streamlit"""
    if df.empty:
        return {
            'total':0,
            'indigencia':0,
            'pobreza':0,
            'no_pobres':0
        }
    
    bajo_indigencia=df[df['ITF'] < cbi]
    bajo_pobreza=df[(df['ITF'] >= cbi) & (df['ITF'] < cbt)]
    no_pobres=df[df['ITF'] >= cbt]

    #SE CALCULA USANDO PONDIH PORQUE A DIFERENCIA DE PONDERA TIENE CORRECCION AJUSTADA POR NO RESPUESTA DE INGRESOS
    total = df['PONDIH'].sum()
    indigencia = bajo_indigencia['PONDIH'].sum()
    pobreza = bajo_pobreza['PONDIH'].sum()
    no_pobres = no_pobres['PONDIH'].sum()

    return {
        'total': total,
        'indigencia': indigencia,
        'pobreza': pobreza,
        'no_pobres': no_pobres
    }