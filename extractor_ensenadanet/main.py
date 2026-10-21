"""Script principal que ejecuta todos los scripts como librerías."""

from scraper_ensenada import ciclo_scraper
from linkapi import enviar_enlaces
from basedatos import guardar_en_bd


def ejecutar_pipeline():
    """Ejecuta el flujo completo: Extracción -> API -> Base de Datos."""
    print("Iniciando pipeline de extracción y envío...")

    # Ejecuta el scraper (extrae, compara con caché y guarda los JSON)
    ciclo_scraper()

    # Ejecuta el adaptador API (lee el JSON nuevo, recorta URLs y envía)
    print("\nConectando con la API del equipo...")
    enviar_enlaces()

    # Ejecuta el guardado en la base de datos PostgreSQL
    print("\nGuardando datos en PostgreSQL...")
    guardar_en_bd()

    print("\nCiclo de ejecución completado.")

if __name__ == "__main__":
    ejecutar_pipeline()
