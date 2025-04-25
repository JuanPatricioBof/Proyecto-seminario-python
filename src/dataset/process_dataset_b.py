"""SECCION B : información a obtener: consultas al dataset principal, del 9 al 13"""

import csv
from utils.constants import diccionario_aglomerados
def informar_aglomerados_punto11(path_procesado):
    

    #Pedir al usuario que seleccione un año, y busque en el último trimestre almacenado del mencionado año, el aglomerado con mayor porcentaje de viviendas de “Material precario” y el aglomerado con menor porcentaje de viviendas de “Material precario”.
    anio=input("Ingrese el año que desea consultar: ")
    if not anio.isdigit():
      print("Por favor, ingrese un año válido.")
      return
    datos=[]#aca se van a guardar los datos  correspondientes al año consultado
    with path_procesado.open('r',encoding='utf-8') as file_csv:
        reader=csv.DictReader(file_csv,delimiter=';')
        for row in reader:
            if row['ANO4']==str(anio):
                datos.append(row)
    if not datos: #si no hay cargados datos de ese año
        print(f"No hay datos cargados para el año {anio}.")
        return
    
    ultimo_trimestre=max(int(row['TRIMESTRE']) for row in datos) #se busca el trimestre mas alto en datos

    #tenemos que filtrar las filas que corresponden al ultimo trimestre del año consultado
    datos_ultimo_trimestre=[row for row in datos if int(row['TRIMESTRE'])==ultimo_trimestre]

    #crear diccionarios para contar las viviendas de material precario por aglomerado
    viviendas_totales={}
    viviendas_precarias={}
    for row in datos_ultimo_trimestre:
        print(row['material_techumbre'])
        aglomerado=row['AGLOMERADO']
        if aglomerado not in viviendas_totales:
            viviendas_totales[aglomerado]=0
            viviendas_precarias[aglomerado]=0
        viviendas_totales[aglomerado]+=1
        if row['material_techumbre'].strip().lower()=='material precario':
            viviendas_precarias[aglomerado]+=1
    #Ahora debemos calcular el porcentaje de viviendas precarias por aglomerado
    porcentajes={}
    for aglomerado in viviendas_totales:
        porcentaje=(viviendas_precarias[aglomerado]/viviendas_totales[aglomerado])*100
        porcentajes[aglomerado]=porcentaje #guardamos el porcentaje en el diccionario
    
    max_aglomerado=max(porcentajes, key=porcentajes.get) #buscamos el aglomerado con mayor porcentaje
    min_aglomerado=min(porcentajes, key=porcentajes.get) #buscamos el aglomerado con menor porcentaje
    
    print(f'\nTrimestre analizado: {ultimo_trimestre} del año {anio}')
    print(f'El algomerado con mayor porcentaje de viviendas de material precario es {diccionario_aglomerados.get(str(max_aglomerado),'DESCONOCIDO')} con : ({porcentajes[max_aglomerado]:.2f}%)')
    print(f'El algomerado con menor porcentaje de viviendas de material precario es {diccionario_aglomerados.get(str(min_aglomerado),'DESCONOCIDO')} con : ({porcentajes[min_aglomerado]:.2f}%)')