"""
Script principal del módulo CESPE.
Coordina la recolección de URLs, envío a la API y la extracción de datos en una sola pasada.
"""

import json
import integracionApi
from extractor_cespe import extract_fields
from links_nuevoCESPE import ciclo_scraper


def ejecutar_todo():
    print("==========================================")
    print("   INICIANDO MÓDULO EXTRACTOR CESPE      ")
    print("==========================================")

    # 1. Recolección de enlaces y actualización de archivos JSON
    print("\n1. Recolectando URLs de CESPE...")
    ciclo_scraper()

    # 2. Transmisión de enlaces a la API
    print("\n2. Enviando enlaces a la API...")
    integracionApi.enviar_a_api()

    # 3. Prueba de extracción de fechas y ubicaciones
    print("\n3. Probando extracción de datos geográficos y fechas...")
    ejemplo_texto = {
        "source": "CESPE",
        "url": "https://www.cespe.gob.mx/public/Noticias/ejemplo",
        "retrieved_at": "2026-10-07T12:00:00",
        "text": "Suspension de servicio el martes 13 en Avenida Reforma y colonia Centro.",
    }
    resultado = extract_fields(ejemplo_texto)
    print(json.dumps(resultado, indent=4, ensure_ascii=False))

    print("\n==========================================")
    print("   PROCESO COMPLETO EJECUTADO CON ÉXITO   ")
    print("==========================================")


if __name__ == "__main__":
    ejecutar_todo()