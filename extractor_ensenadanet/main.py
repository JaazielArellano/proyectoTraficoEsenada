"""Script principal que ejecuta todos los scripts como librerías."""

from scraper_ensenada import ciclo_scraper
from linkapi import enviar_enlaces


def ejecutar_pipeline():
    """Ejecuta el flujo completo: Extracción -> Filtrado -> Envío API."""
    print("Iniciando pipeline de extracción y envío...")

    # Ejecuta el scraper (extrae, compara con caché y guarda los JSON)
    ciclo_scraper()

    # Ejecuta el adaptador API (lee el JSON nuevo, recorta URLs y envía)
    print("\nConectando con la API del equipo...")
    enviar_enlaces()

    print("\nCiclo de ejecución completado.")

if __name__ == "__main__":
    ejecutar_pipeline()
