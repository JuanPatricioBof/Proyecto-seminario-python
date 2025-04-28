
import importlib.readers
from src.utils.constants import DATA_PATH, DATA_OUT_PATH

import csv

import src.dataset.colums_individuo as generar_individuo

import src.dataset.colums_hogar as generar_hogar

import importlib

importlib.reload(generar_individuo)
importlib.reload(generar_hogar)

def join_data(encuesta):
    """genera un único archivo csv, puede ser de hogares o individuos"""

    # generar path al archivo único e identificar que escuesta estoy unificando
    if encuesta == "hogar":
        path_archivos_unidos = DATA_OUT_PATH / "usu_hogar.csv"
        patron_nombre = "usu_hogar_*"
    else:
        path_archivos_unidos = DATA_OUT_PATH / "usu_individual.csv"
        patron_nombre = "usu_individual_*"
    
    # Para controlar que el encabezado se escriba una sola vez
    se_escribio_encabezado = False  
    
    # abro el archivo único para escribirlo
    with path_archivos_unidos.open('w', newline="", encoding = "utf-8") as salida:

        writer = csv.writer(salida, delimiter=';')

        #recorro las carpetas que contiene data_eph
        for path_trimestre in DATA_PATH.iterdir():
            
            #recorro archivos de un trimestre, solo los que quiero unir --> tipo = hogar || individual
            for path_archivo in path_trimestre.glob(patron_nombre):
                
                # abro el csv a copiar 
                with path_archivo.open('r', encoding='utf-8') as entrada:


                    reader = csv.reader(entrada, delimiter=';')     #genero iterable
                    try:
                       header = next(reader)   #separo encabezado
                       print(f"Procesando: {path_archivo.name}")   #debug
                    except StopIteration:
                          print(f"El archivo {path_archivo.name} está vacío.")
                          continue
                
                    if not se_escribio_encabezado:
                        writer.writerow(header)
                        se_escribio_encabezado = True

                    for row in reader:
                        writer.writerow(row)
    print("Dataset único")

def generar_columnas_individual():
    """En esta función agrego columnas nuevas al dataset unido de individual.
    La primera columna que agrego lo hago a partir del original y el nuevo.
    El resto lo sobreescribo en el nuevo.
    """
    path_archivo_unico = DATA_OUT_PATH / "usu_individual.csv"
    path_archivo_procesado = DATA_OUT_PATH / "individual_process.csv"
    
    generar_individuo.generar_columna_CH04_str(path_archivo_unico, path_archivo_procesado)
    

def generar_columnas_hogar():
    """En esta función agrego columnas nuevas al dataset unido hogar.
    La primera columna que agrego lo hago a partir del original y el nuevo.
    El resto lo sobreescrivo en el nuevo.
    """
    path_archivo_unico = DATA_OUT_PATH / "usu_hogar.csv"
    path_archivo_procesado = DATA_OUT_PATH / "hogar_process.csv"
    
    #llamo a funciones de agregar columnas
    generar_hogar.generate_column_tipo_hogar(path_archivo_unico, path_archivo_procesado)    
    generar_hogar.generate_column_material_techumbre(path_archivo_procesado)
    generar_hogar.generate_column_CONDICION_DE_HABITABILIDAD(path_archivo_procesado)