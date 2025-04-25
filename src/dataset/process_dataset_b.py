"""SECCION B : información a obtener: consultas al dataset principal, del 9 al 13"""

import csv

from src.utils.constants import diccionario_aglomerados

def tabla_porcentaje(file_csv_individuos):
    """Pedir al usuario que seleccione dos aglomerados y a partir de la información
contenida retornar una tabla que contenga el porcentaje de personas mayores de
edad con secundario incompleto."""
    salida = ''
    for key in diccionario_aglomerados:
        salida += f'{key}: {diccionario_aglomerados[key]}, '     
    print(salida)

    aglo_A = input("Ingrese código de aglomerado:_")
    aglo_B = input("Ingrese código de aglomerado:_")

    tabla = {}

    # Procesar el archivo
    print("Procesando archivo...")

    with file_csv_individuos.open('r', encoding='utf-8')as archivo:
        reader = csv.DictReader(archivo, delimiter=';')

        for row in reader:
            # si la fila es del aglomerado ingresado --> evaluo
            aglo = row['AGLOMERADO']
            cantidad = int(row['PONDERA'])
            
            # si el aglomerado ingresado coincide con el de la fila
            if(aglo == aglo_A or aglo == aglo_B ):
                año = row['ANO4']
                trimestre = row['TRIMESTRE']

                #inicializo
                if año not in tabla:
                    tabla[año] = {}

                if trimestre not in tabla[año]:
                    tabla[año][trimestre] = {}

                if aglo not in tabla[año][trimestre]:
                    tabla[año][trimestre][aglo_A] = {'total': 0, 'cumple': 0, 'porcentaje': 0.0}
                    tabla[año][trimestre][aglo_B] = {'total': 0, 'cumple': 0, 'porcentaje': 0.0}
                
                # sumo los datos
                tabla[año][trimestre][aglo]['total'] += cantidad

                if (row['NIVEL_ED_str'] == 'Secundario incompleto') and ( int( row['CH06'] ) > 60 ):
                    tabla[año][trimestre][aglo]['cumple'] += cantidad

    # calcular porcentaje
    print("Calculando porcentaje...")
    for año in tabla:
        for trimestre in tabla[año]:
            for aglo in tabla[año][trimestre]:
                calculo = (tabla[año][trimestre][aglo]['cumple'] / tabla[año][trimestre][aglo]['total']) * 100
                tabla[año][trimestre][aglo]['porcentaje'] = round(calculo,2)

    # mostrar informacion
    print("Mostrar información...")    

    print(f'Año    Trimestre   {diccionario_aglomerados[aglo_A]}     {diccionario_aglomerados[aglo_B]}') 
    
    for año in sorted(tabla):
        for trimestre in sorted(tabla[año]):
            salida = (f'{año}   {trimestre}    ')
            for aglo in tabla[año][trimestre]:
                salida += str (tabla[año][trimestre][aglo]['porcentaje'] ) + '%    '
            print(salida)


def informar_aglomerados_punto11(path_procesado):
    anio = input("Ingrese el año que desea consultar: ")
    if not anio.isdigit():
        print("Por favor, ingrese un año válido.")
        return

    datos = []
    with path_procesado.open('r', encoding='utf-8') as file_csv:
        reader = csv.DictReader(file_csv, delimiter=';')
        for row in reader:
            if row['ANO4'] == str(anio):
                datos.append(row)

    if not datos:
        print(f"No hay datos cargados para el año {anio}.")
        return

    ultimo_trimestre = max(int(row['TRIMESTRE']) for row in datos)
    datos_ultimo_trimestre = [row for row in datos if int(row['TRIMESTRE']) == ultimo_trimestre]

    viviendas_totales = {}
    viviendas_precarias = {}

    for row in datos_ultimo_trimestre:
        aglomerado = row['AGLOMERADO']
        tipo_material = row['material_techumbre'].strip().lower()

        if aglomerado not in viviendas_totales:
            viviendas_totales[aglomerado] = 0
            viviendas_precarias[aglomerado] = 0

        viviendas_totales[aglomerado] += 1
        if tipo_material == 'material precario':
            viviendas_precarias[aglomerado] += 1

    porcentajes = {}
    for aglo in viviendas_totales:
        porcentaje = (viviendas_precarias[aglo] / viviendas_totales[aglo]) * 100
        porcentajes[aglo] = porcentaje

    # ⚠️ NO filtramos por diccionario. Usamos todos los aglomerados con datos.
    max_aglomerado = max(porcentajes, key=porcentajes.get)
    min_aglomerado = min(porcentajes, key=porcentajes.get)

    nombre_max = diccionario_aglomerados.get(str(max_aglomerado), f"DESCONOCIDO ({max_aglomerado})")
    nombre_min = diccionario_aglomerados.get(str(min_aglomerado), f"DESCONOCIDO ({min_aglomerado})")

    print(f"\nTrimestre analizado: {ultimo_trimestre} del año {anio}")
    print(f"El aglomerado con mayor porcentaje de viviendas de material precario es {nombre_max} con: ({porcentajes[max_aglomerado]:.2f}%)")
    print(f"El aglomerado con menor porcentaje de viviendas de material precario es {nombre_min} con: ({porcentajes[min_aglomerado]:.2f}%)")