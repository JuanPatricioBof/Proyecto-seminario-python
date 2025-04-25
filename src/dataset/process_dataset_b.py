"""SECCION B : información a obtener: consultas al dataset principal, del 9 al 13"""

import csv

from src.utils.constants import AGLOMERADOS_NOMBRES

def tabla_porcentaje(file_csv_individuos):
    """Pedir al usuario que seleccione dos aglomerados y a partir de la información
contenida retornar una tabla que contenga el porcentaje de personas mayores de
edad con secundario incompleto."""
    salida = ''
    for key in AGLOMERADOS_NOMBRES:
        salida += f'{key}: {AGLOMERADOS_NOMBRES[key]}, '     
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

    print(f'Año    Trimestre   {AGLOMERADOS_NOMBRES[aglo_A]}     {AGLOMERADOS_NOMBRES[aglo_B]}') 
    
    for año in sorted(tabla):
        for trimestre in sorted(tabla[año]):
            salida = (f'{año}   {trimestre}    ')
            for aglo in tabla[año][trimestre]:
                salida += str (tabla[año][trimestre][aglo]['porcentaje'] ) + '%    '
            print(salida)
