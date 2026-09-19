# Módulo REQUEST — Validación de datos (El Vigía)

## Qué hace
El módulo REQUEST recibe el JSON que entregan los extractores (X, CFE, Ensenada.net, Facebook) ya con las entidades detectadas (fecha, día, calle, colonia, índice de confianza) y **valida esos datos antes de que se guarden en PostgreSQL**.

## Entrada
Un objeto JSON con la estructura acordada por el equipo:

```json
{
  "source": "X",
  "url": "https://x.com/ejemplo/1",
  "retrieved_at": "2026-09-18T10:00:00",
  "text": "texto original de la publicación",
  "date": "2026-09-18",
  "day": "viernes",
  "street": "Avenida Reforma",
  "neighborhood": "Zona Centro",
  "confidence": 0.90
}
```

## Qué valida
1. **Campos obligatorios**: `source`, `url`, `retrieved_at`, `text`, `confidence` no pueden venir vacíos.
2. **Confianza**: `confidence` debe estar entre 0 y 1.
3. **Fecha y día**: si `date` viene, debe tener formato `YYYY-MM-DD`, y `day` debe coincidir con el día de la semana real de esa fecha.
4. **Geografía**: `street` y `neighborhood`, si vienen, deben existir en el catálogo de calles/colonias de Ensenada. Si ambos vienen vacíos, el registro no se puede ubicar y se marca inválido.

## Salida
Un resultado con `valido` (true/false) y la lista de `errores` encontrados, para que el módulo de almacenamiento decida si el registro pasa a PostgreSQL o se descarta/reporta.

## Cómo correrlo
Solo usa librerías estándar de Python (`json`, `datetime`), no requiere instalar nada:

```bash
python semana2.py
```
