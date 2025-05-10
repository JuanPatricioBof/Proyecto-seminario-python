"""funciones para agregar columnas"""

import csv

def generate_column_tipo_hogar(archivo_original, archivo_procesado):
    """Se debe generar una nueva columna llamada TIPO_HOGAR que indica el tipo de hogar:
    "Unipersonal" (una persona).
    "Nuclear" (2 a 4 personas).
    "Extendido" (5 o más personas)."""
    try:
        #Abrir el archivo y leer el contenido:
        with archivo_original.open('r',encoding='utf-8') as file_csv:
            reader=csv.DictReader(file_csv,delimiter=';')
            fieldnames=reader.fieldnames
            if fieldnames is None:
                raise ValueError
            
            #Se agrega la nueva columna
            if('tipo_hogar') not in fieldnames:
                fieldnames.append('tipo_hogar')
        
            filas=[]
            for row in reader:
                if int(row['IX_TOT'])==1:
                    row['tipo_hogar']='Unipersonal'
                elif 2<= int(row['IX_TOT'])<=4:
                    row['tipo_hogar']='Nuclear'
                else:
                    row['tipo_hogar']='Extendido'
                filas.append(row)
              
    except FileNotFoundError:
        print(f"Error: el archivo no fue encontrado") 
    except PermissionError:
        print(f"Error: acceso de lectura denegado")
    except ValueError:
        print(f"Error: archivo vacío")
    else:
        # Sobrescribir el archivo con los datos nuevos
        try:
            with archivo_procesado.open('w', newline = "", encoding='utf-8')as file_csv:
                writer = csv.DictWriter(file_csv, fieldnames=fieldnames, delimiter=';')
                writer.writeheader()
                writer.writerows(filas)
        except PermissionError:
            print(f"Error: permiso de escritura denegado")
        else:
            print("✅ Se agregó la columna tipo_hogar con valores traducidos.")
        

def generate_column_material_techumbre(archivo_procesado):
    #Se debe generar una nueva columna llamada MATERIAL_TECHUMBRE que indica el tipo de hogar basado en el campo V4:
    #- 5 a 7: "Material precario".
    #- 1 a 4: "Material durable".
    # 9: “No aplica”.
    try:
        with archivo_procesado.open('r',encoding='utf-8')as file_csv:
            reader=csv.DictReader(file_csv,delimiter=';')
            fieldnames=reader.fieldnames

            if fieldnames is None:
                raise ValueError
            
            #Se agrega la nueva columna
            if('material_techumbre') not in fieldnames:
                fieldnames.append('material_techumbre')
            filas=[]
            for row in reader:
                if row['IV4'].strip() in ['5','6','7']:
                    row['material_techumbre']='Material precario'
                elif row['IV4'].strip() in ['1','2','3','4']:
                    row['material_techumbre']='Material durable'
                elif row['IV4'].strip()=='9':
                    row['material_techumbre']='No aplica'                
                filas.append(row)

    except FileNotFoundError:
        print(f"Error: el archivo no fue encontrado")
    except PermissionError:
        print(f"Error: permiso de lectura denegado")
    except ValueError:
        print(f"Error: archivo vacío")
    else:
        try:
            with archivo_procesado.open('w', newline = "", encoding='utf-8')as file_csv:
                    writer = csv.DictWriter(file_csv, fieldnames=fieldnames, delimiter=';')
                    writer.writeheader()
                    writer.writerows(filas)
        except PermissionError:
            print(f"Error: el acceso de escritura denegado")
        else:
            print("✅ Se agregó la columna material_techumbre con valores traducidos.")


def generar_columna_densidad_hogar(path_copia_hogar):
    """ Genera una nueva columna denominada DENSIDAD_HOGAR según el
        siguiente criterio:

        Bajo: menos de 1 persona por habitación.
        Medio: entre 1 y 2 personas por habitación.
        Alto: más de 2 personas por habitación.
        Desconocido: información insuficiente.

        Para la generación se utilizan las columnas IX_TOT, que indica
        la cantidad total de miembros del hogar, e IV2, que indica la
        cantidad de habitaciones de la vivienda (sin contar baño/s,
        cocina, pasillo/s, lavadero, garage). En caso de faltar la
        información de alguna de las columnas o estar mal cargadas, la
        nueva columna se marca como 'Desconocido'.

        En caso de ya existir, la columna se actualiza.
"""
    try:
        with open(path_copia_hogar, "r", encoding="utf-8") as file:

            # Guardo el encabezado y una lista con las filas
            csv_reader = csv.DictReader(file, delimiter=";")
            header = csv_reader.fieldnames
            rows = list(csv_reader)
        
        if header is None:
            raise ValueError
    
    except FileNotFoundError:
        print(f"Error: archivo no encontrado")
    except PermissionError:
        print(f"Error: acceso al archivo denegado")
    except ValueError:
        print(f"Error: archivo vacío")
    else:
        # Actualizo el encabezado en caso de ser necesario
        if not "DENSIDAD_HOGAR" in header:
            header.append("DENSIDAD_HOGAR")

        # Compruebo que existan las columnas necesarias
        if not {"IX_TOT","IV2"}.issubset(header):
                print(f"Error: falta una o más columnas para el procesamiento"
                    " de los datos")
        else:
            # Actualizo las filas calculando la densidad según
            # La cantidad de miembros y habitaciones
            for row in rows:
                miembros = row["IX_TOT"]
                habitaciones = row["IV2"]
                if(miembros.isnumeric() and habitaciones.isnumeric()):
                    miembros = int(miembros)
                    habitaciones = int(habitaciones)
                    if(miembros < habitaciones):
                        row["DENSIDAD_HOGAR"] = "Bajo"
                    elif(miembros <= habitaciones*2):
                        row["DENSIDAD_HOGAR"] = "Medio"
                    else:
                        # Más de dos miembros por habitación
                        row["DENSIDAD_HOGAR"] = "Alto"
                else:
                    # Faltan datos o están mal cargados
                    row["DENSIDAD_HOGAR"] = "Desconocido"

            # Sobreescirbo el archivo con los datos actualizados
            try:
                with open(path_copia_hogar, "w", newline = "") as file:
                    csv_writer = csv.DictWriter(file, fieldnames=header, delimiter=";")
                    csv_writer.writeheader()
                    csv_writer.writerows(rows)
            except PermissionError:
                print(f"Error. Acceso de escritura denegado")
            else:
                print(f"✅ Se agregó la columna DENSIDAD_HOGAR")



def clasificar_condicion_habitabilidad(agua, origen_agua, tiene_banio, ubicacion_banio, desague_banio, piso, inodoro):
    """
    Genera la columna CONDICION_DE_HABITABILIDAD según reglas basadas en IV6, IV7, IV8, IV9, IV11 y IV3.
    Insuficiente:
    (IV6 = 3) o (IV8 = 2) o (IV11 = 4) o (IV3 ≠ 1 y 2) o (IV9 = 3) o (IV7 ≠ 1, 2 y 3).
    Regular:
    (IV6 = 2) o (IV7 = 3) o (IV9 = 2) o (IV10 = 2 y 3) o (IV11 = 2 y 3) o (IV3 ≠ 1 y 2).
    Saludables:
    (IV6 = 1 y 2) y (IV7 = 1 y 2) y (IV8 = 1) y (IV9 = 1) y (IV3 = 1 y 2) y (IV11 = 1 y 2) y (IV10 = 1)
    Buena: 
    (IV6 = 1) y (IV7 = 1) y (IV8 = 1) y (IV9 = 1) y (IV3 = 1) y (IV11 = 1) y (IV10 = 1)
    """
    # Condición BUENA
    if (agua == '1' and origen_agua == '1' and tiene_banio == '1' and
        ubicacion_banio == '1' and desague_banio == '1' and piso == '1' and inodoro == '1'):
        return 'buena'

    # Condición SALUDABLE
    elif (agua in ['1', '2'] and origen_agua in ['1', '2'] and tiene_banio == '1' and
          ubicacion_banio == '1' and desague_banio in ['1', '2'] and piso in ['1', '2'] and inodoro == '1'):
        return 'saludable'

    # Condición REGULAR
    elif ((agua == '2' or origen_agua == '3' or inodoro in ['2', '3'] or ubicacion_banio == '2' or
           desague_banio in ['2', '3'] or piso not in ['1', '2'])):
        return 'regular'

    # Condición INSUFICIENTE
    elif (agua == '3' or tiene_banio == '2' or desague_banio == '4' or
          piso not in ['1', '2'] or ubicacion_banio == '3' or origen_agua not in ['1', '2', '3']):
        return 'insuficiente'

def generate_column_CONDICION_DE_HABITABILIDAD(archivo_procesado):
    """Genera la columna CONDICION_DE_HABITABILIDAD según reglas basadas en IV6, IV7, IV8, IV9, IV11 y IV3."""
    with open(archivo_procesado, 'r', encoding='utf-8') as file_csv:
        reader = csv.DictReader(file_csv, delimiter=';')
        fieldnames = reader.fieldnames

        if 'CONDICION_DE_HABITABILIDAD' not in fieldnames:
            fieldnames.append('CONDICION_DE_HABITABILIDAD')

        filas = []
        for row in reader:
            agua = row['IV6']
            origen_agua = row['IV7']
            tiene_banio = row['IV8']
            ubicacion_banio = row['IV9']
            desague_banio = row['IV11']
            piso = row['IV3']
            inodoro = row['IV10']

            row['CONDICION_DE_HABITABILIDAD'] = clasificar_condicion_habitabilidad(agua, origen_agua, tiene_banio, ubicacion_banio, desague_banio, piso, inodoro)

            filas.append(row)

    with open(archivo_procesado, 'w', newline='', encoding='utf-8') as file_csv:
        writer = csv.DictWriter(file_csv, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        writer.writerows(filas)

    print("✅ Se agregó la columna CONDICION_DE_HABITABILIDAD.")


