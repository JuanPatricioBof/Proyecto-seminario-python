
import importlib.readers
from src.utils.constants import DATA_PATH, DATA_OUT_PATH

import csv

import src.dataset.colums_individuo as generar_individuo

import src.dataset.colums_hogar as generar_hogar

import importlib

import re

importlib.reload(generar_individuo)
importlib.reload(generar_hogar)

def join_data(encuesta):
    """Genera un único archivo csv, puede ser de hogares o individuos"""

    # generar path al archivo único e identificar qué encuesta estoy unificando
    if encuesta == "hogar":
        path_archivos_unidos = DATA_OUT_PATH / "usu_hogar.csv"
        patron_nombre = "usu_hogar_*"
    else:
        path_archivos_unidos = DATA_OUT_PATH / "usu_individual.csv"
        patron_nombre = "usu_individual_*"
    
    # Para controlar que el encabezado se escriba una sola vez
    se_escribio_encabezado = False  

    # Extraer año y trimestre del nombre de la carpeta
    def extraer_ano_trimestre(path):
        nombre = path.name
        match = re.search(r'(\d)er_Trim_(\d{4})', nombre)
        if match:
            trimestre = int(match.group(1))
            ano = int(match.group(2))
            return (ano, trimestre)
        return (0, 0)

    # Ordenar carpetas de data_eph por año y trimestre descendente
    carpetas_trimestres = sorted(
        [p for p in DATA_PATH.iterdir() if p.is_dir()],
        key=extraer_ano_trimestre,
        reverse=True
    )

    try:
        # Abro el archivo único para escribirlo
        with path_archivos_unidos.open('w', newline="", encoding='utf-8') as salida:
            writer = csv.writer(salida, delimiter=';')

            # Recorro carpetas ordenadas
            for path_trimestre in carpetas_trimestres:
                # Recorro archivos del tipo deseado dentro de la carpeta
                for path_archivo in path_trimestre.glob(patron_nombre):
                    try:        
                        with path_archivo.open('r', encoding='utf-8') as entrada:
                            reader = csv.reader(entrada, delimiter=';')
                            try:
                                header = next(reader)  # separo encabezado
                                print(f"Procesando: {path_archivo.name}")
                            except StopIteration:
                                print(f"El archivo {path_archivo.name} está vacío.")
                                continue

                            if not se_escribio_encabezado:
                                writer.writerow(header)
                                se_escribio_encabezado = True

                            for row in reader:
                                writer.writerow(row)
                    except PermissionError:  
                        print(f"Error: permiso de lectura a {path_archivo} denegado")
                    # no hace falta chequear FileNotFoundError porque si
                    # entró en el for el archivo seguro existe
    except PermissionError:
        print(f"Error: acceso de escritura a {path_archivos_unidos} denegado.")
    else:
        print("Dataset único generado.")

def generar_columnas_individual():
    """En esta función agrego columnas nuevas al dataset unido de individual.
    La primera columna que agrego lo hago a partir del original y el nuevo.
    El resto lo sobreescribo en el nuevo.
    """
    path_archivo_unico = DATA_OUT_PATH / "usu_individual.csv"
    path_archivo_procesado = DATA_OUT_PATH / "individual_process.csv"
    
    generar_individuo.generar_columna_CH04_str(path_archivo_unico, path_archivo_procesado )
    generar_individuo.generate_columna_NIVEL_ED_str(path_archivo_procesado)
    generar_individuo.generate_columna_CONDICION_LABORAL(path_archivo_procesado)
    generar_individuo.generar_columna_universitario_completo(path_archivo_procesado)
    #generar_individuo.generar_columna_X(path_archivo_procesado)
    

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
    generar_hogar.generar_columna_densidad_hogar(path_archivo_procesado)