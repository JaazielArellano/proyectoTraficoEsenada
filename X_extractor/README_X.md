# Módulo Extractor para X (Twitter) Trabajo Extratron

En mi módulo de Extractor X, mi codigo recibe el texto de una noticia que encuentre en X  y se encarga de buscar y extraer automáticamente 4 datos clave: fecha, día de la semana, calle y colonia. Tambien calcula un porcentaje de confianza para indicar qué tan completa viene la información.

#Entradas y salidas del Código

1.- Entrada
El programa recibe un diccionario con el texto ya extraído de la publicación de X:

{
  "source": "X (Twitter)",
  "url": "[https://x.com/Argumento_X/status/2095281615396061580](https://x.com/Argumento_X/status/2095281615396061580)",
  "retrieved_at": "2026-09-09T12:50:00",
  "text": "Choque vial este martes 15 de septiembre en Avenida Reforma, colonia Centro."
}

2.- Salida 
Nos da de resultado un JSON con los datos que nos pidieron. Si no se encuentra alguno de los datos ese espacio se rellena como NULL

{
  "date": "2026-09-15",
  "day": "martes",
  "street": "Avenida Reforma",
  "neighborhood": "Centro",
  "confidence": 1.0
}

Las herramientas que utilice fue Python 3.13 y la app de X 
