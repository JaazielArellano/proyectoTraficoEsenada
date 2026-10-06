"""Script principal que ejecuta los scripts como librerías."""

# Importación de los módulos del proyecto
import enviar_post
import extractor_vigia
import url


def ejecutar_todo():
    """Ejecuta los tres módulos del proyecto."""
    # Ejecuta el módulo encargado de procesar las URLs
    print("1. Ejecutando url.py")
    url.ejecutar()

    # Ejecuta el módulo encargado de enviar los enlaces
    print("\n2. Ejecutando enviar_post.py")
    enviar_post.ejecutar()

    # Ejecuta el módulo de extracción de datos de la página El Vigía
    print("\n3. Ejecutando extractor_vigia.py")
    extractor_vigia.ejecutar()

    # Confirmación de finalización
    print("==========================================")
    print("Proceso completo ejecutado")


# Ejecutar el script directamente
if __name__ == "__main__":
    ejecutar_todo()
