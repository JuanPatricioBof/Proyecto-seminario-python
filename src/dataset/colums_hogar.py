import csv

def generate_column_tipo_hogar(archivo_original, archivo_procesado):
    #Se debe generar una nueva columna llamada TIPO_HOGAR que indica el tipo de hogar:
    #"Unipersonal" (una persona).
    #"Nuclear" (2 a 4 personas).
    #"Extendido" (5 o más personas).
    #Abrir el archivo y leer el contenido:
    with archivo_original.open('r',encoding='utf-8') as file_csv:
        reader=csv.DictReader(file_csv,delimiter=';')
        fieldnames=reader.fieldnames

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

    # Sobrescribir el archivo con los datos nuevos
    with archivo_procesado.open('w', newline = "", encoding='utf-8')as file_csv:
        writer = csv.DictWriter(file_csv, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        writer.writerows(filas)
    print("✅ Se agregó la columna tipo_hogar con valores traducidos.")
    

def generate_column_material_techumbre(archivo_procesado):
    #Se debe generar una nueva columna llamada MATERIAL_TECHUMBRE que indica el tipo de hogar basado en el campo V4:
    #- 5 a 7: "Material precario".
    #- 1 a 4: "Material durable".
    # 9: “No aplica”.
    with archivo_procesado.open('r',encoding='utf-8')as file_csv:
        reader=csv.DictReader(file_csv,delimiter=';')
        fieldnames=reader.fieldnames

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
    with archivo_procesado.open('w', newline = "", encoding='utf-8')as file_csv:
            writer = csv.DictWriter(file_csv, fieldnames=fieldnames, delimiter=';')
            writer.writeheader()
            writer.writerows(filas)
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
            try:
                # Guardo el encabezado y una lista con las filas
                csv_reader = csv.DictReader(file, delimiter=";")
                header = csv_reader.fieldnames
                rows = list(csv_reader)
            except StopIteration:
                print(f"Error: Archivo vacío")
    except FileNotFoundError:
        print(f"Error: archivo no encontrado")
    except PermissionError:
        print(f"Error: acceso al archivo denegado")
    else:
        # Actualizo el encabezado en caso de ser necesario
        if not "DENSIDAD_HOGAR" in header:
            header.append("DENSIDAD_HOGAR")
        print(header)
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
                if(miembros.isnumeric and habitaciones.isnumeric):
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
            print(f"Columna 'DENSIDAR_HOGAR' generada.")
