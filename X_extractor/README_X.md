Módulo: Extractor para X (Twitter) Trabajo Extratron
Alumno: Muñiz Tavarez Arturo
Materia: Patrones de Comportamiento
Grupo:371 


En mi módulo de Extractor X, mi codigo recibe el texto de una noticia que encuentre en X  y se encarga de buscar y extraer automáticamente 4 datos clave: fecha, día de la semana, calle y colonia. 
Tambien calcula un porcentaje de confianza para indicar qué tan completa viene la información.

Este modulo se encarga de procesar la información de las noticias.

Se deben buscar publicaciones reales de noticias en X (Twitter) sobre accidentes o cierres viales y se entrega un JSON con la URL, el nombre de la fuente y la fecha de consulta.

{
  "date": "2026-09-15",
  "day": "martes",
  "street": "Avenida Reforma",
  "neighborhood": "Centro",
  "confidence": 1.0
}

