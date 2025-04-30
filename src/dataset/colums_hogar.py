import csv

def generar_columna_densidad_hogar(path_copia_hogar):
    """ Genera una nueva columna denominada DENSIDAD_HOGAR según el siguiente 
        criterio:

        Bajo: menos de 1 persona por habitación.
        Medio: entre 1 y 2 personas por habitación.
        Alto: más de 2 personas por habitación.
        Desconocido: información insuficiente.

        Para la generación se utilizan las columnas IX_TOT, que indica la cantidad
        total de miembros del hogar, e IV2, que indica la cantidad de habitaciones
        de la vivienda (sin contar baño/s, cocina, pasillo/s, lavadero, garage).
        En caso de faltar la información de alguna de las columnas o estar 
        mal cargadas, la nueva columna se marca como 'Desconocido'.

        En caso de ya existir, la columna se actualiza.
"""
    try:
        with open(path_copia_hogar, "r", encoding="utf-8") as file:
            try:
                # guardo el encabezado y una lista con las filas
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
        # actualizo el encabezado en caso de ser necesario
        if not "DENSIDAD_HOGAR" in header:
            header.append("DENSIDAD_HOGAR")
        print(header)
        # compruebo que existan las columnas necesarias
        if not {"IX_TOT","IV2"}.issubset(header):
                print(f"Error: falta una o más columnas para el procesamiento"
                      " de los datos")
        else: 
            # actualizo las filas calculando la densidad según 
            # la cantidad de miembros y habitaciones
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
                        # más de dos miembros por habitación
                        row["DENSIDAD_HOGAR"] = "Alto"
                else:
                    # faltan datos o están mal cargados
                    row["DENSIDAD_HOGAR"] = "Desconocido"

        # sobreescirbo el archivo con los datos actualizados
        try:
            with open(path_copia_hogar, "w", newline = "") as file:
                csv_writer = csv.DictWriter(file, fieldnames=header, delimiter=";")
                csv_writer.writeheader()
                csv_writer.writerows(rows)
        except PermissionError:
            print(f"Error. Acceso de escritura denegado")
        else:
            print(f"Columna 'DENSIDAR_HOGAR' generada.")
