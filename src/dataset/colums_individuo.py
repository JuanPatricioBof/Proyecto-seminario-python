import csv

def generar_columna_universitario_completo(path_copia_individual):
    """ genera una nueva columna llamada UNIVERSITARIO numérica que
    indica si una persona mayor de edad ha completado, como mínimo, el
    nivel universitario. 
    
    Los valores de la columna son:
    - "1": Sí.
    - "0": No.
    - "2": No aplica.
    - "": Indefinido (sin información suficiente).

    Para la generación se utilizan las columnas "NIVEL_ED", "CH12" y
    "CH13".

    Se considera que la persona completó el nivel universitario si
    cumple al menos una de las siguientes condiciones:
    - Su nivel educativo está registrado como universitario completo
    (valor 6 en la columna "NIVEL_ED").
    - Cursó por última vez el nivel universitario o superior (valor
    7 u 8 en la columna "CH12"), y, en caso de haber cursado por último
    el nivel universitario, completó ese nivel. (valor 7 en la columna
     "CH12" y valor 1 en la columna "CH13").

    Si la columna ya existe, actualiza los datos de la misma.
    """

    # accedo al encabezado y a las filas del archivo
    try:
        with open(path_copia_individual, "r", encoding="utf-8") as file:
            try:
                csv_reader = csv.DictReader(file,delimiter=";")
                header = csv_reader.fieldnames
                rows = list(csv_reader)
            except StopIteration:
                print(f"Error: Archivo vacío.")
    except FileNotFoundError:
        print(f"Error: El archivo no se encontró")
    except PermissionError:
        print(f"Error: Acceso de lectura denegado")
    else:
        #actualizo el encabezado
        if not "UNIVERSITARIO" in header:
            header.append("UNIVERSITARIO")

        # compruebo que el archivo contenga las columnas necesarias
        if not {"CHO6", "CH12", "NIVEL_ED"}.issubset(header):
            print(f"Error: no se encontraron una o más columnas necesarias"
                    " para el procesamiento")
        else:
            # actualizo las filas
            for row in rows:
                edad = row["CH06"]
                if(edad.isnumeric):
                    if(int(edad) >= 18):
                        if(row["NIVEL_ED"] == "6" or (row["CH12"] == "8" or
                          (row["CH12"] == "7" and row["CH13"] == "1"))):
                            row["UNIVERSITARIO"] = "1"  # sí
                        else:
                            row["UNIVERSITARIO"] = "0"  # no
                    else:
                        row["UNIVERSITARIO"] = "2"  # no aplica
                else:
                    row["UNIVERSITARIO"] = "" # indefinido

        # sobreescribo el archivo con los cambios
        try:
            with open(path_copia_individual, "w", newline = "") as file:
                csv_writer = csv.DictWriter(file, fieldnames=header,
                                            delimiter=";")
                csv_writer.writeheader()
                csv_writer.writerows(rows)
        except PermissionError:
            print(f"Error. El archivo no puede ser sobreeescrito")
        else:
            print(f"Columna 'UNIVERSITARIO_COMPLETO' generada")
