
 Descripción General

# Responsabilidades Principales
- [Responsabilidad 1:  Descarga de páginas web y normalización de texto] [3, 4]
- [Responsabilidad 2:  Detección de calles, colonias y fechas mediante reglas/regex] [5]
- [Responsabilidad 3:  Validación geográfica, endpoints REST o gestión de esquemas en PostgreSQL] [5, 6]

# Contratos de Entrada y Salida (Interfaces)
Para garantizar la comunicación desacoplada entre módulos [2, 7]:

# Entrada Esperada (Contrato de Entrada)
```json
{
  "source": "cfe",
 "url": "https://www.cfe.mx/avisos/mantenimiento_zona_centro",
  "retrieved_at": "2026-09-15T10:00:00",
  "text": "Texto limpio a procesar..."
}

Salida Producida (Contrato de Salida)

{
  "date": "2026-09-15",
  "day": "martes",
  "street": "Avenida Reforma",
  "neighborhood": "Centro",
  "confidence": 0.95
}
 Instalación y Ejecución Independiente
Instrucciones para desplegar y probar este módulo por separado sin depender de otros componentes:

    Requisitos e Instalación de Dependencias:

pip install -r requirements.txt

    Configuración de Variables de Entorno: Crear un archivo .env local. Nunca incluir contraseñas ni claves secretas en el código.
    Ejecución:

python main.py

    Pruebas Unitarias:

pytest


