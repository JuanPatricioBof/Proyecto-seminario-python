import csv
import json
from pathlib import Path
from src.utils.constants import DATA_PATH, DATA_OUT_PATH


def leer_eph(path_archivo: Path):
    """Función generadora que devuelve primero los encabezados y luego cada registro."""
    archivo_eph = path_archivo.open('r', encoding='utf-8')
    reader = csv.DictReader(archivo_eph, delimiter=';')
    try:
        header = reader.fieldnames  # ← Este es el header real (lista de strings)
        yield header                 # ← Lo devolvés primero
        for registro in reader:
            yield registro
    except Exception as e:
        raise Exception(f"Problemas con el archivo {path_archivo.name}: {e}")
    finally:
        archivo_eph.close()


def verificar_anio_trimestre(path_archivo: Path, anio, trimestre) -> bool:
    """Consulta en el json si el archivo fue agregado al dataset único"""

    info_anio_trimestre = {}
    existe_anio_trimestre = False
    try:
        with path_archivo.open('r', encoding='utf-8') as archivo:
            info_anio_trimestre = json.load(archivo)
            if anio in info_anio_trimestre:
                if trimestre in info_anio_trimestre[anio]:
                    existe_anio_trimestre = True
                else:
                    info_anio_trimestre[anio].append(trimestre)
            else:
                info_anio_trimestre[anio] = [trimestre]
    except FileNotFoundError:
        info_anio_trimestre = {anio: [trimestre]}
    finally:
        try:
            # Ordenar JSON
            info_anio_trimestre = {
                anio: sorted(trimestres, key=int, reverse=True)
                for anio, trimestres in sorted(info_anio_trimestre.items(), key=lambda x: -int(x[0]))
            }
            # Guardar JSON actualizado
            with path_archivo.open('w', encoding='utf-8') as archivo:
                json.dump(info_anio_trimestre, archivo, indent=2)
        except Exception as e:
            raise Exception(f"Error al escribir en el archivo {path_archivo.name}: {e}")

    return existe_anio_trimestre # FIX: No agregar el año y trimestre si no existe hasta que el recorrido de la eph finalice OK
def limpiar_na(val):
    """Limpia valores NA, reemplazándolos por un string vacío."""
    return "" if val is None or val == "NA" else val


def join_data():
    """Crea dataset único de para encuesta de hogares y para encuesta de individuos.
    También crea un json para cada tipo de encuesta donde se registran los años y trimestres procesados."""

    path_csv = {'hogar': DATA_OUT_PATH / "usu_hogar.csv", 'individual': DATA_OUT_PATH / "usu_individual.csv"}
    path_json = {'hogar':DATA_OUT_PATH / "estructura_hogares.json", 'individual': DATA_OUT_PATH / "estructura_individuos.json"}
    patron_hogar = "hogar"
    patron_individual = ["individual","persona"]
    primer_header_hogar = None
    primer_header_individual = None
    for path_archivo in DATA_PATH.glob(f'**/*.txt'):
        try:
            eph_actual = leer_eph(path_archivo)
        except ValueError as e:
            continue

        if patron_hogar in path_archivo.name.lower(): # TODO Cambiar
            header_actual = next(eph_actual)
            primer_registro = next(eph_actual)
            if primer_header_hogar is None:
                primer_header_hogar = header_actual
            else:
                if set(header_actual)!= set(primer_header_hogar):
                     print("Header esperado:", primer_header_hogar)
                     print("Header encontrado:", header_actual)
                     print( f"¡Error! Header inconsistentes en {path_archivo}. Se omitirá." )
                     continue
            anio = primer_registro["ANO4"]
            trimestre = primer_registro["TRIMESTRE"]
            if not verificar_anio_trimestre(path_json['hogar'], anio, trimestre):
                try:
                    with path_csv['hogar'].open('a', newline='', encoding='utf-8') as f_csv_ind:
                            writer_csv = csv.DictWriter(f_csv_ind, delimiter=';', fieldnames=primer_header_hogar)
                            if path_csv['hogar'].stat().st_size == 0:
                                writer_csv.writeheader()
                            nuevo_registro = [limpiar_na(primer_registro[campo]) for campo in writer_csv.fieldnames]
                            nuevo_registro_dict = dict(zip(writer_csv.fieldnames, nuevo_registro))
                            writer_csv.writerow(nuevo_registro_dict)
                            for registro in eph_actual:
                                nuevo_registro = [limpiar_na(registro[campo]) for campo in writer_csv.fieldnames]
                                nuevo_registro_dict = dict(zip(writer_csv.fieldnames, nuevo_registro))
                                writer_csv.writerow(nuevo_registro_dict)
                except Exception as e:
                    raise Exception(f"Error al escribir en el archivo {path_csv['hogar'].name}: {e}")
    
        elif any(p in path_archivo.name.lower() for p in patron_individual): # TODO Cambiar
            header_actual = next(eph_actual)
            primer_registro = next(eph_actual)
            anio = primer_registro["ANO4"]
            trimestre = primer_registro["TRIMESTRE"]
            if primer_header_individual is None:
                primer_header_individual = header_actual
            else:
                if set(header_actual)!= set(primer_header_individual):
                     print("Header esperado:", primer_header_individual)
                     print("Header encontrado:", header_actual)
                     print( f"¡Error! Header inconsistentes en {path_archivo}. Se omitirá." )
                     continue
            if not verificar_anio_trimestre(path_json['individual'], anio, trimestre):
                try:
                    with path_csv['individual'].open('a', newline='', encoding='utf-8') as f_csv_ind:
                            writer_csv = csv.DictWriter(f_csv_ind, delimiter=';', fieldnames=primer_header_individual)
                            if path_csv['individual'].stat().st_size == 0:
                                writer_csv.writeheader()
                            nuevo_registro = [limpiar_na(primer_registro[campo]) for campo in writer_csv.fieldnames]
                            nuevo_registro_dict = dict(zip(writer_csv.fieldnames, nuevo_registro))
                            writer_csv.writerow(nuevo_registro_dict)
                            for registro in eph_actual:
                                nuevo_registro = [limpiar_na(registro[campo]) for campo in writer_csv.fieldnames]
                                nuevo_registro_dict = dict(zip(writer_csv.fieldnames, nuevo_registro))
                                writer_csv.writerow(nuevo_registro_dict)
                except Exception as e:
                    raise Exception(f"Error al escribir en el archivo {path_csv['individual'].name}: {e}")

        else:
            raise ValueError(f"El archivo {path_archivo.name} no es un archivo válido de EPH.")




