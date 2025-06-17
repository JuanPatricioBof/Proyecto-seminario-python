from pathlib import Path

PROJECT_PATH = Path(__file__).parent.parent.parent # Path to the proyect root directory

DATA_PATH = PROJECT_PATH / "files" /"data_eph" # Path to the "data_eph" directory

DATA_OUT_PATH = PROJECT_PATH / "files" /"data_out" # Path to the "data_out" directory

JSON_HOGARES_PATH = DATA_OUT_PATH / "estructura_hogares.json"

JSON_INDIVIDUOS_PATH = DATA_OUT_PATH / "estructura_individuos.json"

diccionario_aglomerados={
    '02' : 'Gran La Plata',
    '03' : 'Bahía Blanca - Cerri',
    '04' : 'Gran Rosario',
    '05' : 'Gran Santa Fé',
    '06' : 'Gran Paraná',
    '07' : 'Posadas',
    '08' : 'Gran Resistencia',
    '09' : 'Comodoro Rivadavia - Rada Tilly',
    '10' : 'Gran Mendoza',
    '12' : 'Corrientes',
    '13' : 'Gran Córdoba',
    '14' : 'Concordia',
    '15' : 'Formosa',
    '17' : 'Neuquén - Plottier',
    '18' : 'Santiago del Estero - La Banda',
    '19' : 'Jujuy - Palpalá',
    '20' : 'Río Gallegos',
    '22' : 'Gran Catamarca',
    '23' : 'Gran Salta',
    '25' : 'La Rioja',
    '26' : 'Gran San Luis',
    '27' : 'Gran San Juan',
    '29' : 'Gran Tucumán - Tafí Viejo',
    '30' : 'Santa Rosa - Toay',
    '31' : 'Ushuaia - Río Grande',
    '32' : 'Ciudad Autónoma de Buenos Aires',
    '33' : 'Partidos del GBA',
    '34' : 'Mar del Plata',
    '36' : 'Río Cuarto',
    '38' : 'San Nicolás - Villa Constitución',
    '91' : 'Rawson - Trelew',
    '93' : 'Viedma- Carmen de Patagones',
    }
