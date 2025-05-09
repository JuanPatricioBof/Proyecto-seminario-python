"""funciones para agregar columnas"""

import csv

def generar_columna_CH04_str(archivo_original, archivo_procesado):
    """Se traduce los valores CH04 numéricos a "Masculino" y "Femenino" según corresponda. El resultado se debe 
    almacenar en una nueva columna llamada CH04_str.
    Recorre el archivo original y guarda cada linea, con la nueva columna, en una variable auxliar.
    Luego abre el archivo nuevo y carga con esta variable.
       """
    try:
        # leo el contenido y genero los datos nuevos en la memoria
        with archivo_original.open('r', encoding='utf-8') as entrada:

            reader = csv.DictReader(entrada, delimiter=';')
            fieldnames = reader.fieldnames  # obtiene el encabezado
            
            if fieldnames is None:
                raise ValueError
            
            # Agrego la nueva columna si no está
            if "CH04_str" not in fieldnames:
                fieldnames.append("CH04_str")
            
            #cargo todos los datos en una lista que representan las las filas del archivo
            filas = [] 
            for row in reader:
                row['CH04_str'] = ('Masculino' if row['CH04']=='1' else 'Femenino')
                filas.append(row)

    except FileNotFoundError:
        print(f"Error: archivo no encontrado")
    except PermissionError:
        print(f"Error: acceso de lectura denegado")
    except ValueError:
        print(f"Error: archivo vacío")
    else:
        try:
            # cargo los datos nuevos en el archivo nuevo de individual
            with archivo_procesado.open('w', newline = "", encoding='utf-8')as salida:
                writer = csv.DictWriter(salida, fieldnames=fieldnames, delimiter=";")
                writer.writeheader()
                writer.writerows(filas)
        except PermissionError:
            print(f"Error: acceso de escritura denegado")
        else:
            print("✅ Se agregó la columna CH04_str.")


def generate_columna_NIVEL_ED_str(path_nuevo):
    """Se traduce los valores NIVEL_ED numéricos a descripciones en formato texto según las reglas especificadas.
       El resultado se debe almacenar en una nueva columna llamada NIVEL_ED_str.
    """
    try:
        # leo el contenido y genero los datos nuevos en la memoria
        with path_nuevo.open('r', encoding='utf-8') as file_csv:

            reader = csv.DictReader(file_csv, delimiter=';')
            fieldnames = reader.fieldnames
            
            if fieldnames is None:
                raise ValueError
        

            # Agrego la nueva columna si no está
            if "NIVEL_ED_str" not in fieldnames:
                fieldnames.append("NIVEL_ED_str")
            
            filas = []  # para guardar los datos nuevos
            for row in reader:
                # Traducir los valores de NIVEL_ED
                nivel_ed = row['NIVEL_ED']
                if nivel_ed == '1':
                    row['NIVEL_ED_str'] = "Primario incompleto"
                elif nivel_ed == '2':
                    row['NIVEL_ED_str'] = "Primario completo"
                elif nivel_ed == '3':
                    row['NIVEL_ED_str'] = "Secundario incompleto"
                elif nivel_ed == '4':
                    row['NIVEL_ED_str'] = "Secundario completo"
                elif nivel_ed in ['5', '6']:
                    row['NIVEL_ED_str'] = "Superior o universitario"
                else:
                    row['NIVEL_ED_str'] = "Desconocido"  # Por si hay algún valor fuera de las reglas

                filas.append(row)
    except FileNotFoundError:
        print(f"Error: archivo no encontrado")
    except PermissionError:
        print(f"Error: acceso de lectura denegado")
    except ValueError:
        print(f"Error: archivo vacío")
    else:
        try:
            # Sobrescribir el archivo con los datos nuevos
            with path_nuevo.open('w', newline="", encoding='utf-8') as file_csv:
                writer = csv.DictWriter(file_csv, fieldnames=fieldnames, delimiter=";")
                writer.writeheader()
                writer.writerows(filas)
        except PermissionError:
            print(f"Error: acceso de escritura denegado")
        else:
            print("✅Se agrego la columna NIVEL_ED_str")


def generate_columna_CONDICION_LABORAL(path_nuevo):
    """Agrega una columna llamada CONDICION_LABORAL con valores de texto según las reglas dadas."""

    try:
        with path_nuevo.open('r', encoding='utf-8') as file_csv:
            reader = csv.DictReader(file_csv, delimiter=';')
            fieldnames = reader.fieldnames

            if fieldnames is None:
                raise ValueError
            
            if "CONDICION_LABORAL" not in fieldnames:
                fieldnames.append("CONDICION_LABORAL")

            filas = []
            for row in reader:
                estado = row['ESTADO']
                cat_ocup = row['CAT_OCUP']

                if estado == '1' and cat_ocup in ('1', '2'):
                    row['CONDICION_LABORAL'] = "Ocupado autónomo"
                elif estado == '1' and cat_ocup in ('3', '4', '9'):
                    row['CONDICION_LABORAL'] = "Ocupado dependiente"
                elif estado == '2':
                    row['CONDICION_LABORAL'] = "Desocupado"
                elif estado == '3':
                    row['CONDICION_LABORAL'] = "Inactivo"
                elif estado == '4':
                    row['CONDICION_LABORAL'] = "Fuera de categoría/sin información"
                else:
                    row['CONDICION_LABORAL'] = "Sin información"

                filas.append(row)

    except FileNotFoundError:
        print(f"Error: archivo no encontrado")
    except PermissionError:
        print(f"Error: acceso de lectura denegado")
    except ValueError:
        print(f"Error: archivo vacío")
    else:
        try:
            with path_nuevo.open('w', newline='', encoding='utf-8') as file_csv:
                writer = csv.DictWriter(file_csv, fieldnames=fieldnames, delimiter=';')
                writer.writeheader()
                writer.writerows(filas)
        except PermissionError:
            print(f"Error: acceso de escritura denegado")
        else:
            print("✅Se agrega la columna CONDICION_LABORAL")


def generar_columna_universitario_completo(path_nuevo):
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
        with open(path_nuevo, "r", encoding="utf-8") as file:
            csv_reader = csv.DictReader(file,delimiter=";")
            header = csv_reader.fieldnames
            if header is None:
                raise ValueError
                
            rows = list(csv_reader)
            
    except FileNotFoundError:
        print(f"Error: El archivo no se encontró")
    except PermissionError:
        print(f"Error: Acceso de lectura denegado")
    except ValueError:
        print(f"Error: archivo vacío")
    else:
        # No hubo excepciones
        # Actualizo el encabezado
        if not "UNIVERSITARIO" in header:
            header.append("UNIVERSITARIO")

        # compruebo que el archivo contenga las columnas necesarias
        if not {"CH06", "CH12", "NIVEL_ED"}.issubset(header):
            print(f"Error: no se encontraron una o más columnas necesarias"
                    " para el procesamiento")
        else:
            # actualizo las filas
            for row in rows:
                edad = row["CH06"]
                if(edad.isnumeric()):
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
                with open(path_nuevo, "w", encoding="utf-8", newline = "") as file:
                    csv_writer = csv.DictWriter(file, fieldnames=header,
                                                delimiter=";")
                    csv_writer.writeheader()
                    csv_writer.writerows(rows)
            except PermissionError:
                print(f"Error. El archivo no puede ser sobreeescrito")
            else:
                print(f"✅Se agregó la columna UNIVERSITARIO_COMPLETO")


