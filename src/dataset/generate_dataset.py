
from src.utils.constants import DATA_PATH, DATA_OUT_PATH

import csv

def join_data(encuesta):
    """genera un único archivo csv, puede ser de hogares o individuos"""

    # generar path al archivo único e identificar que escuesta estoy unificando
    if encuesta == "hogar":
        path_archivo_unico = DATA_OUT_PATH / "usu_hogar.csv"
        patron_nombre = "usu_hogar_*"
    else:
        path_archivo_unico = DATA_OUT_PATH / "usu_individual.csv"
        patron_nombre = "usu_individual_*"
    
    # Para controlar que el encabezado se escriba una sola vez
    se_escribio_encabezado = False  
    
    # abro el archivo único para escribirlo
    with path_archivo_unico.open('w', newline="", encoding = "utf-8") as salida:

        writer = csv.writer(salida, delimiter=';')

        #recorro las carpetas que contiene data_eph
        for path_trimestre in DATA_PATH.iterdir():
            
            #recorro archivos de un trimestre, solo los que quiero unir --> tipo = hogar || individual
            for path_archivo in path_trimestre.glob(patron_nombre):
                
                # abro el csv a copiar 
                with path_archivo.open('r', encoding='utf-8') as entrada:

                    print(f"Procesando: {path_archivo.name}")   #debug

                    reader = csv.reader(entrada, delimiter=';')     #genero iterable

                    header = next(reader)   #separo encabezado
                    
                    if not se_escribio_encabezado:
                        writer.writerow(header)
                        se_escribio_encabezado = True

                    for row in reader:
                        writer.writerow(row)
