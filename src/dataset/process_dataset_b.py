"""SECCION B : información a obtener: consultas al dataset principal, del 8 al 13"""

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

def universitarios_en_viviendas_insuficientes(DATA_OUT_PATH):
    hogar_path = DATA_OUT_PATH / "hogar_process.csv"
    individual_path = DATA_OUT_PATH / "individual_process.csv"

    anio = input("Ingrese el año que desea consultar: ")
    if not anio.isdigit():
        print("Por favor, ingrese un año válido.")
        return

    # Leer datos del hogar
    datos_hogar = []
    with open(hogar_path, encoding='utf-8') as f_hog:
        reader = csv.DictReader(f_hog, delimiter=';')
        for row in reader:
            if row['ANO4'] == anio:
                datos_hogar.append(row)

    if not datos_hogar:
        print(f"No hay datos cargados para el año {anio}.")
        return

    # Obtener el último trimestre disponible
    ultimo_trimestre = max(int(row['TRIMESTRE']) for row in datos_hogar)

    # Filtrar viviendas con condición de habitabilidad insuficiente
    codusus_insuficientes = {
        row['CODUSU'] for row in datos_hogar
        if int(row['TRIMESTRE']) == ultimo_trimestre and row['CONDICION_DE_HABITABILIDAD'] == 'insuficiente'
    }

    # Leer datos del individual
    datos_individual = []
    with open(individual_path, encoding='utf-8') as f_ind:
        reader = csv.DictReader(f_ind, delimiter=';')
        for row in reader:
            if row['ANO4'] == anio and int(row['TRIMESTRE']) == ultimo_trimestre:
                datos_individual.append(row)

    # Contar personas con NIVEL_ED en ['5', '6'] que vivan en esas viviendas
    contador = sum(
        1 for row in datos_individual
        if row['CODUSU'] in codusus_insuficientes and row['NIVEL_ED'] in ['5', '6']
    )

    print(f"\nAño {anio} - Trimestre {ultimo_trimestre}:")
    print(f"Cantidad de personas con nivel universitario o superior en viviendas 
          con condición insuficiente: {contador}")

def regiones_segun_porcentaje_inquilinos(hogar_path):
    """ Recibe la ruta al archivo e informa en orden las regiones en orden
        descendiente según su porcentaje de inquilinos. 
        El porcentaje de inquilinos de cada región se calcula en base a la
        cantidad de inquilinos (valor 3 en la columna "II7") sobre la cantidad
        total de hogares de esa región. """

    def region_str(num_region):
        """Recibe el numero de región y lo traduce a texto según lo acordado en
            el diseño de la EPH. En caso de encontrar un valor no válido, marca
            la región como "Indefinida" """
        match num_region:
            case 1:
                ans = "Gran Buenos Aires"
            case 40:
                ans = "Noroeste"
            case 41:
                ans = "Noreste"
            case 42:
                ans = "Cuyo"
            case 43:
                ans = "Pampeana"
            case 44:
                ans = "Patagonia"
            case _:
                ans = "Indefinida"
        return ans

    try:
        with hogar_path.open("r", encoding = "utf-8") as file:
            csv_reader = csv.DictReader(file, delimiter = ";")
            header = csv_reader.fieldnames

            if header is None:
                # archivo vacio
                raise ErrorValue
            
            if not({"REGION","II7","PONDERA"}.issubset(header)):
                raise KeyError
            
            # data_hogar[region]: [cant_hogares_totales, cant_inquilinos]
            data_hogar = {}
            
            for row in csv_reader:
                region = row["REGION"]

                # si no está cargada la región, la agrego
                if not region in data_hogar:
                    data_hogar[region] = [0, 0] 
                
                 # guardo hogares totales
                data_hogar[region][0] += row["PONDERA"] 

                # guardo inquilinos
                if(row["II7"] == 3):
                    data_hogar[region][1] += row["PONDERA"]  

    except FileNotFound:
        print(f"Error: el archivo no fue encontrado")
    except PermissionError:
        print(f"Error: permiso de lectura denegado")
    except ValueError:
        print(f"Error: archivo vacío")
    except KeyError:
        print(f"Error de formato: faltan una o más columnas para el procesamiento")
    else:
        # ordeno en orden descendente según porcentaje
        data_hogar = dict(sort(data_hogar.items(), key = lambda item: 
                         (float(item[1][1]*100)/float(item[1][0])), reverse = True))
        
        # Imprimo los datos ya ordenados
        print(f"Regiones según su porcentaje de inquilinos: ")
        for region, valores in data_hogar:
            print(f"{region_str(region)}. ({(float(valores[1]*100)/float(valores[0]))}%)")
                
def jubilados_condicion_habitabilidad_insuficiente(DATA_OUT_PATH):
    # pendiente : agregar docstring

    hogar_path = DATA_OUT_PATH / "hogar_process.csv"
    individual_path = DATA_OUT_PATH / "individual_process.csv"

    try:
        file_hogar = open(hogar_path,"r",encoding="utf-8")
        file_individual = open(hogar_path,"r",encoding="utf-8")

        reader_h = csv.DictReader(file_hogar, delimiter=";")
        reader_i = csv.DictReader(file_individual, delimiter=";")

        header_h = reader_h.fieldnames
        header_i = reader_i.fieldnames

        # compruebo que el archivo no esté vacío
        if(header_h == None or header_i == None):
            raise ValueError

        ult_anio = 0
        ult_trim = 0

        fila_h = next(reader_h, None)
        fila_i = next(reader_i, None)
        coincidencia = False

        # compruebo que existan todas las columnas que necesito

        if not({"ANO4","TRIMESTRE","PONDERA","CODUSU","ESTADO",
                "CAT_INACT"}.issubset(header_i)):
            raise KeyError

        if not({"ANO4","TRIMESTRE","PONDERA","CODUSU","AGLOMERADO",
                "CONDICION_DE_HABITABILIDAD"}.issubset(header_h)):
            raise KeyError

        # busco que coincidan el ult año y trimestre
        while not(fila_h is None) and not(fila_i is None) and
        not(coincidencia):  
            if(fila_h["ANO4"] == fila_i["ANO4"] and 
            fila_h["TRIMESTRE"] == fila_i["TRIMESTRE"]):
                coincidencia = True       
            # comparo primero por año y despues por trimestre
            # avanzo el más nuevo porque las fechas van en orden descendente
            elif(fila_h["ANO4"], fila_h["TRIMESTRE"]) <
               (fila_i["ANO4"], fila_i["TRIMESTRE"]):
               fila_i = next(reader_i, None)
            else:
                fila_h = next(reader_h, None)
        
        # si no encuentro un archivo hogar e individual del mismo trimestre,
        # no se pueden generar los datos
        if not(coincidencia):
            raise KeyError

        # llegue al año y trimestre que necesito
        anio = reader_i["ANO4"]
        trimestre = reader_i["TRIMESTRE"]
        
        # data_jubilados[codigo_identificacion] = ponderacion
        data_jubilados = {}
        while(not fila_i is None)and(anio == fila_i["ANO4"] and trimestre == fila_i["TRIMESTRE"]):
            if(fila_i["ESTADO"]=="3" and fila_i["CAT_INAC"] == "1"):

                data_jubilados[fila_i["CODUSU"]] = fila_i["PONDERA"]
            fila_i = next(reader_i, None)

        file_individual.close()

        # guarda para cada nro de aglomerado, una lista con la cant total de
        # jubilados y la cant de jubilados con condicion de habitabilidad insuficiente
        jubilados_por_aglomerado = {}
        while(not fila_h is None)and(anio == fila_h["ANO4"] and trimestre == fila_h["TRIMESTRE"]):
            if(fila_h["CODUSU"] in data_jubilados):
                # si todavía no se cargó informacion del aglomerado, lo agrego
                if not(fila_h["AGLOMERADO"] in jubilados_por_aglomerado):
                    jubilados_por_aglomerado[fila_h["AGLOMERADO"]] = [0,0]  
            
                # sumo al total de jubilados
                jubilados_por_aglomerado[fila_h["AGLOMERADO"]][0] += data_jubilados["CODUSU"]
                
                # sumo a la cant de jubilados con condicion insuficiente
                if(fila_h["CONDICION_DE_HABITABILIDAD"]=="insuficiente"):
                    jubilados_por_aglomerado[fila_h["AGLOMERADO"]][1] += data_jubilados["CODUSU"]
            fila_h = next(reader_i, None)

        file_hogar.close()

    except FileNotFoundError:
        print(f"Error: archivo no encontrado")
    except PermissionError:
        print(f"Error: acceso de lectura al archivo denegado")
    except ValueError:
        print(f"Error: archivo vacío")
    except KeyError:
        print(f"Error: faltan datos para el procesamiento")
    else:
        #imprimo el porcentaje para cada aglomerado
        print(f"Porcentaje de jubilados en condición de habitabilidad insuficiente:")
        for nro_aglomerado in diccionario_aglomerado:
            if not(nro_aglomerado in jubilados_por_aglomerado):
                print(f"{diccionario_aglomerado[nro_aglomerado]}: sin datos")
            else:
                # porcentaje = condicion_insuficiente*100 / total
                porcentaje = float(float(jubilados_por_aglomerado[nro_aglomerado][1]*100)/
                                   float(jubilados_por_aglomerado[nro_aglomerado[0]]))
                print(f"{diccionario_aglomerado[nro_aglomerado]}: {porcentaje}%")




                
            