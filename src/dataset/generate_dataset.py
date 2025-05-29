
import importlib.readers
from src.utils.constants import DATA_PATH, DATA_OUT_PATH

import csv

import src.dataset.colums_individuo as generar_individuo

import src.dataset.colums_hogar as generar_hogar

import importlib

import re
import json
from pathlib import Path
from collections import defaultdict
importlib.reload(generar_individuo)
importlib.reload(generar_hogar)


def join_data(encuesta):
    """Genera archivos CSV y JSON unificados"""
    # Configuración de paths (igual que antes)
    if encuesta == "hogar":
        path_csv = DATA_OUT_PATH / "usu_hogar.csv"
        path_json = DATA_OUT_PATH / "estructura_hogar.json"
        patron_nombre = "usu_hogar_*"
    else:
        path_csv = DATA_OUT_PATH / "usu_individual.csv"
        path_json = DATA_OUT_PATH / "estructura_individual.json"
        patron_nombre = "usu_individual_*"
    
    datos = []
    headers = None
    estructura = defaultdict(list)

    # Procesar archivos 
    for path_archivo in DATA_PATH.glob(f"**/{patron_nombre}"):
        with path_archivo.open('r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=';')
            # Verificacion  para el primer archivo
            if headers is None:
                # Chequeo estricto de encabezados
                if any(h in [None, ''] for h in reader.fieldnames):
                    continue  # Pasa al siguiente archivo
                headers = reader.fieldnames
            
            # Verificación para archivos posteriores
            current_headers = reader.fieldnames
            if current_headers != headers:
                continue
                
            for row in reader:    
                datos.append(row)
                año = row['ANO4']
                trimestre = row['TRIMESTRE']
                if trimestre not in estructura[año]:
                     estructura[año].append(trimestre)

    if not datos:
        print("No se encontraron datos válidos")
        return

    # Ordenar datos 
    datos_ordenados = sorted(
        datos,
        key=lambda x: (-int(x['ANO4']), -int(x['TRIMESTRE'])))

    # Escribir CSV 
    with path_csv.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers, delimiter=';')
        writer.writeheader()
        
        # Filtrado final preventivo
        for row in datos_ordenados:
            writer.writerow(row)

    # Escribir JSON 
    estructura_ordenada = {
        año: sorted(trimestres, key=int, reverse=True)
        for año, trimestres in sorted(estructura.items(), key=lambda x: -int(x[0]))
    }
    
    with path_json.open('w', encoding='utf-8') as f:
        json.dump(estructura_ordenada, f, indent=2)
    
    print(f"Archivos generados exitosamente")

        
        
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
    generar_hogar.generate_column_CONDICION_DE_HABITABILIDAD(path_archivo_procesado)

