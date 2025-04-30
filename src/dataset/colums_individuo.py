import csv
from pathlib import Path

# ruta a copia provisional para testear el funcionamiento de la funcion
ruta_datos = Path().resolve().parent.parent
ruta_datos = ruta_datos / "files" / "data_eph" / "EPH_usu_3er_Trim_2024_txt" 
ruta_individual = ruta_datos / "usu_individual_T324_copia.txt"

def generar_universitario_completo(path_copia_csv):
    """ genera una nueva columna llamada UNIVERSITARIO numérica que indica si
    una persona mayor de edad ha completado el como mínimo el nivel 
    universitario. Si la columna ya existe, actualiza los datos de la misma.
    Los datos de la columna se representan de la siguiente manera:
    "1": Sí.
    "0": No.
    "2": No aplica.
    "": Indefinido (sin información suficiente).
    Se considera que la persona ha completado el nivel universitario si:
    - Su nivel educativo está registrado como universitario completo (columna
    "NIVEL_ED")
    ó
    - Cursó por última vez el nivel universitario o superior. En caso de haber 
    cursado por último el nivel universitario, completó ese nivel. (Columnas
    "CH12" y "CH13")
    """

    # accedo al encabezado y a las filas del archivo
    try:
        with open(path_copia_csv, "r", encoding="utf-8") as file:
            try:
                csv_reader = csv.DictReader(file,delimiter=";")
                header = csv_reader.fieldnames
                rows = list(csv_reader)
            except StopIteration:
                print(f"Error: Archivo vacío.")
                exit(1)
    except FileNotFoundError:
        print(f"Error: El archivo no se encontró")
        exit(1)
    except PermissionError:
        print(f"Error: Incapaz de acceder al archivo")
        exit(1)
    #actualizo el encabezado 
    if not "UNIVERSITARIO" in header:
        header.append("UNIVERSITARIO")

    # actualizo las filas
    for row in rows:
        try:
            edad = row["CH06"]
            if(edad.isnumeric):
                if(int(edad) >= 18):
                    if((row["CH12"] =="8" or (row["CH12"] =="7" and 
                    row["CH13"] == "1")) or row["NIVEL_ED"] == "6"):
                        row["UNIVERSITARIO"] = "1" # sí
                    else:
                        row["UNIVERSITARIO"] = "0" # no
                else:
                    row["UNIVERSITARIO"] = "2" # no aplica
            else:
                row["UNIVERSITARIO"] = "" # indefinido
        except KeyError:
            print(f"Error: no se encontraron una o más columnas necesarias"
                  " para el procesamiento")


  
    # sobreescribo el archivo con los cambios
    # no verifico que no exista o esté vacío porque si fuese así ya habría terminado la función antes
    try: 
        with open(path_copia_csv, "w", newline = "") as file:
            csv_writer = csv.DictWriter(file,fieldnames=header,delimiter=";")
            csv_writer.writeheader()
            csv_writer.writerows(rows)
    except PermissionError:
        print(f"Error. El archivo no puede ser sobreeescrito")
    else:
        print("Columna generada")

# codigo provisional para testear el funcionamiento de la funcion
generar_universitario_completo(ruta_individual)