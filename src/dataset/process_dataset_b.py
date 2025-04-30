"""SECCION B : información a obtener: consultas al dataset principal, del 9 al 13"""

import csv
from collections import defaultdict
from src.utils.constants import diccionario_aglomerados

def tabla_nivel_educativo_por_aglomerado_EJ_9B(individual_path):
    # Pedir al usuario que elija un aglomerado
    aglomerado_elegido = input("Ingrese el código del aglomerado a consultar: ").strip()

    # Creamos una tabla donde la clave es (año, trimestre)
    # y el valor es otro diccionario que cuenta personas por nivel educativo
    tabla = defaultdict(lambda: defaultdict(int))

    with open(individual_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            if row['AGLOMERADO'] != aglomerado_elegido:
                continue  # Filtrar por el aglomerado elegido

            try:
                edad = int(row['CH06'])
                if edad < 18:
                    continue  # Solo mayores de edad

                año = int(row['ANO4'])
                trimestre = int(row['TRIMESTRE'])
                nivel_ed = int(row['NIVEL_ED'])
                pondera = int(row['PONDERA'])

                clave = (año, trimestre)
                tabla[clave][nivel_ed] += pondera  # Sumamos con el peso muestral
            except (ValueError, KeyError):
                continue  # Saltear filas con datos faltantes o mal formateados

    # Encabezado
    print("\nTabla de mayores de edad por nivel educativo (ponderado):")
    print("Año | Trimestre | Sin instr. | Prim. Inc. | Prim. Comp. | Sec. Inc. | Sec. Comp. | Sup. Univ.")

    # Ordenar por año y trimestre descendente
    for (año, trim) in sorted(tabla.keys(), reverse=True):
        niveles = tabla[(año, trim)]
        fila = [
            año,
            trim,
            niveles.get(7, 0),  # Sin instrucción
            niveles.get(1, 0),  # Primario incompleto
            niveles.get(2, 0),  # Primario completo
            niveles.get(3, 0),  # Secundario incompleto
            niveles.get(4, 0),  # Secundario completo
            niveles.get(5, 0) + niveles.get(6, 0)  # Universitario (incompleto + completo)
        ]
        print("{:<4} | {:<9} | {:<11} | {:<10} | {:<12} | {:<10} | {:<11} | {:<11}".format(*fila))
        
        
        
        
def informar_tabla_porcentaje_10B(file_csv_individuos):
    """Pedir al usuario que seleccione dos aglomerados y a partir de la información
contenida retornar una tabla que contenga el porcentaje de personas mayores de
edad con secundario incompleto."""
    """ Estructura de la variable tabla: 
    { 
        año: {
            trimestre: {
                    agloA: {total:0, cumple:0, porcentaje:0.0}
                    agloB:  {total:0, cumple:0, porcentaje:0.0}
                }
            trimestre:  {...}
        }
        año: {...} 
    }"""

    #muestro al usuario las opciones de aglomerado (imprimo diccionario de codigo:nombre)
    salida = ''
    for key in diccionario_aglomerados:
        salida += f'{key}: {diccionario_aglomerados[key]}, '     
    print(salida)
    
    #pido al usuario que ingrese data
    aglo_A = input("Ingrese código de aglomerado:_").zfill(2)
    aglo_B = input("Ingrese código de aglomerado:_").zfill(2)

    tabla = {}

    # recorro el archivo procesado 
    print("Procesando archivo...")

    with file_csv_individuos.open('r', encoding='utf-8')as archivo:
        reader = csv.DictReader(archivo, delimiter=';')

        for row in reader:
            # si la fila es del aglomerado ingresado --> evaluo
            aglo = row['AGLOMERADO']
            cantidad = int(row['PONDERA'])
            
            # si es el aglomerado ingresado --> proceso
            if(aglo == aglo_A.lstrip("0") or aglo == aglo_B.lstrip("0") ):
                año = row['ANO4']
                trimestre = row['TRIMESTRE']

                #inicializo
                if año not in tabla:
                    tabla[año] = {}

                if trimestre not in tabla[año]:
                    tabla[año][trimestre] = {}

                if aglo not in tabla[año][trimestre]:
                    tabla[año][trimestre][aglo_A.lstrip("0")] = {'total': 0, 'cumple': 0, 'porcentaje': 0.0}
                    tabla[año][trimestre][aglo_B.lstrip("0")] = {'total': 0, 'cumple': 0, 'porcentaje': 0.0}
                
                # sumo el total de aglomerados
                tabla[año][trimestre][aglo]['total'] += cantidad
                # sumo los aglomerados que cumplen
                #if (row['NIVEL_ED_str'] == 'Secundario incompleto') and ( int( row['CH06'] ) > 60 ):
                if (row['NIVEL_ED'] == '3') and ( int( row['CH06'] ) > 60 ):
                    tabla[año][trimestre][aglo]['cumple'] += cantidad

    # calculo el porcentaje de aglomerado para cada trimestre y año
    print("Calculando porcentaje...")
    for año in tabla:
        for trimestre in tabla[año]:
            for aglo in tabla[año][trimestre]:
                total = tabla[año][trimestre][aglo]['total']
                if total != 0 : 
                    cumple = tabla[año][trimestre][aglo]['cumple']
                    calculo = (cumple / total) * 100
                    tabla[año][trimestre][aglo]['porcentaje'] = round(calculo,2)

    # mostrar informacion
    print("Mostrar información...")    
    # imprimo encabezado de tabla
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
            if row['ANO4'] == anio:
                datos.append(row)

    if not datos:
        print(f"No hay datos cargados para el año {anio}.")
        return

    # Como los datos están ordenados por año y trimestre en forma descendente,
    # el primer registro del año es del trimestre más reciente
    ultimo_trimestre = int(datos[0]['TRIMESTRE'])
    datos_ultimo_trimestre = [
        row for row in datos if int(row['TRIMESTRE']) == ultimo_trimestre
    ]

    viviendas_totales = {}
    viviendas_precarias = {}

    for row in datos_ultimo_trimestre:
        aglomerado = row['AGLOMERADO']
        tipo_material = row['material_techumbre'].strip().lower()

        try:
            pondera = int(row["PONDERA"])
        except ValueError:
            continue  # Saltar si el dato está mal cargado

        if aglomerado not in viviendas_totales:
            viviendas_totales[aglomerado] = 0
            viviendas_precarias[aglomerado] = 0

        viviendas_totales[aglomerado] += pondera
        if tipo_material=='material precario':
            viviendas_precarias[aglomerado] += pondera

    porcentajes = {}
    for aglomerado in viviendas_totales:
        total = viviendas_totales[aglomerado]
        precarias = viviendas_precarias[aglomerado]
        if total > 0:
            porcentajes[aglomerado] = (precarias / total) * 100

    porcentajes_validos = {
        aglo: porcentaje
        for aglo, porcentaje in porcentajes.items()
        if str(aglo) in diccionario_aglomerados
    }

    if not porcentajes_validos:
        print("No se encontraron aglomerados válidos con nombre para mostrar.")
        return

    max_aglomerado = max(porcentajes_validos, key=porcentajes_validos.get)
    min_aglomerado = min(porcentajes_validos, key=porcentajes_validos.get)

    nombre_max = diccionario_aglomerados[str(max_aglomerado)]
    nombre_min = diccionario_aglomerados[str(min_aglomerado)]

    print(f"\nTrimestre analizado: {ultimo_trimestre} del año {anio}")
    print("Porcentaje de viviendas con material precario por aglomerado:")

    for aglo, porcentaje in sorted(porcentajes_validos.items(), key=lambda x: x[1], reverse=True):
        nombre = diccionario_aglomerados[str(aglo)]
        print(f"  - {nombre}: {porcentaje:.2f}%")

    print(f"\nEl aglomerado con mayor porcentaje es {nombre_max} ({porcentajes_validos[max_aglomerado]:.2f}%)")
    print(f"El aglomerado con menor porcentaje es {nombre_min} ({porcentajes_validos[min_aglomerado]:.2f}%)")