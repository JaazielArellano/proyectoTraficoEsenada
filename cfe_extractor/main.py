#CECILIA RUIZ NAVARRO
"""
Archivo Principal (main.py)
 flujo completo del sistema ejecutando los módulos en orden:
1. Extraer enlaces de la CFE y guardarlos localmente.
2. Enviar los enlaces a Ximena (API).
3. Obtener o procesar la respuesta con los datos procesados.
"""

import time

# 1. Importar los scripts como librerías (módulos)
import guardarlinks as extractor
import Collector_CFE as enviador  # O el nombre exacto de tu script para enviar
# import procesar_datos as receptor # Script para procesar los datos de Ximena


def ejecutar_flujo_completo():
    print("==================================================")
    print("INICIANDO FLUJO GENERAL DEL SISTEMA CFE")
    print("==================================================\n")

    # ----------------------------------------------------
    # PASO 1: Extraer enlaces de CFE
    # ----------------------------------------------------
    print(" PASO 1: Ejecutando extracción de enlaces...")
    try:
        # Llamamos a la función de extracción de tu librería
        # Si usas monitoreo de una sola ejecución o de ciclo:
        enlaces = extractor.obtener_enlaces_actuales("https://www.cfe.mx/Pages/default.aspx")
        if enlaces:
            # Guardar en JSON usando la función de tu script
            extractor.guardar_enlaces("links_cfe.json", enlaces)
            print(f"✅ PASO 1 Completado: Se guardaron {len(enlaces)} enlaces.\n")
        else:
            print("⚠️ PASO 1: No se extrajeron enlaces. Continuando...\n")
    except Exception as e:
        print(f"❌ Error en el PASO 1 (Extracción): {e}\n")
        return

    # Pausa de cortesía entre procesos
    time.sleep(2)

    # ----------------------------------------------------
    # PASO 2: Enviar enlaces a Ximena / API
    # ----------------------------------------------------
    print("PASO 2: Enviando enlaces a Ximena...")
    try:
        # Llamamos al código que empaqueta y envía el JSON
        # Asumiendo que tu script de envío tiene una función llamada enviar_datos()
        # O ejecutamos la lógica de envío desde main:
        enviador.enviar_payload_a_api() 
        print(" PASO 2 Completado: Enlaces enviados con éxito.\n")
    except Exception as e:
        print(f"Error en el PASO 2 (Envío): {e}\n")
        return

    time.sleep(2)

    # ----------------------------------------------------
    # PASO 3: Obtener y procesar los datos recibidos
    # ----------------------------------------------------
    print("📌 PASO 3: Extrayendo/Consultando información final de Ximena...")
    try:
        # Aquí llamas a la función de tu tercer código
        # receptor.obtener_respuesta_ximena()
        print("✅ PASO 3 Completado: Proceso finalizado exitosamente.\n")
    except Exception as e:
        print(f" Error en el PASO 3 (Recepción): {e}\n")

    print("==================================================")
    print(" PROCESO COMPLETO FINALIZADO CON ÉXITO")
    print("==================================================")


if __name__ == "__main__":
    ejecutar_flujo_completo()