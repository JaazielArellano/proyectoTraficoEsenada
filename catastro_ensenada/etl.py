"""ETL de vialidades de Ensenada desde el CSV original."""
import csv
import unicodedata
from pathlib import Path

BASE = Path(__file__).resolve().parent
ORIGEN = BASE / 'catastro_ensenada_limpio.csv'
DESTINO = BASE / 'catastro_ensenada.csv'


def normalizar(texto):
    texto = unicodedata.normalize('NFKD', texto.strip().upper())
    return ' '.join(''.join(c for c in texto if not unicodedata.combining(c)).split())


def ejecutar(origen=ORIGEN, destino=DESTINO):
    registros = set()
    with open(origen, newline='', encoding='utf-8-sig') as archivo:
        lector = csv.DictReader(archivo)
        requeridas = {'TIPO_ELEMENTO', 'nomvial', 'tipovial'}
        if not requeridas.issubset(lector.fieldnames or []):
            raise ValueError('Faltan columnas requeridas en el CSV de origen')
        for fila in lector:
            if normalizar(fila['TIPO_ELEMENTO']) != 'VIALIDAD':
                continue
            nombre = normalizar(fila['nomvial'])
            tipo = normalizar(fila['tipovial'])
            if nombre and nombre != 'NINGUNO' and tipo and tipo != 'NINGUNO':
                registros.add((nombre, tipo))
    with open(destino, 'w', newline='', encoding='utf-8') as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(['nombre', 'tipo'])
        escritor.writerows(sorted(registros))
    return len(registros)


if __name__ == '__main__':
    print(f'ETL completado: {ejecutar()} vialidades únicas (nombre y tipo).')
