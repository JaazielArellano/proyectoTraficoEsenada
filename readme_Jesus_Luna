# Módulo de Gráficas

**Autor:** Jesus Luna
**Maestro:** Guillermo Alejandro
**Universidad Autonoma de Baja California**
**Facultad de Ciencias Administrativas y sociales**

Módulo de visualización de datos que genera gráficas interactivas en el navegador con [D3.js](https://d3js.org/), a partir de datos en formato JSON (noticias por categoría, estado e impacto vial).

## Tabla de contenido

- [Descripción]
- [Requisitos]
- [Instalación]
- [Uso]
- [Estructura del código]
- [Tipos de gráficas recomendadas]
- [Solución de problemas]
- [Trabajo pendiente]
- [Notas del autor]
- [Autor](#autor)

## Descripción

D3.js es una biblioteca de JavaScript especializada en la visualización de datos mediante gráficas interactivas. Este módulo recibe los datos como una variable JSON (D3.js soporta JSON y diccionarios) y dibuja una gráfica por cada conjunto de datos.

## Requisitos

- Editor | [Visual Studio Code](https://code.visualstudio.com/) |
- Extensión | **Live Server** (para VS Code) |
- Navegador | Cualquier navegador web moderno |
- Conexión a internet | Necesaria, D3.js se carga desde un CDN |
- Entorno virtual | Python venv |

## Instalación

1. Descargue o clone este proyecto y ábralo en VS Code.
2. Cree y active el entorno virtual desde la terminal del proyecto:

   python -m venv venv

   # Windows
   venv\Scripts\activate

   # macOS / Linux
   source venv/bin/activate
   ```

3. Abra la pestaña de Extensiones (`Ctrl+Shift+X`), busque **Live Server** e instálela.
4. Verifique que el archivo HTML cargue D3.js con la siguiente línea:

   ```html
   <script src="https://d3js.org/d3.v7.min.js"></script>
   ```

## Uso

1. Abra el archivo `pako.html` en VS Code.
2. Haga clic derecho y seleccione **Open with Live Server**.
3. El navegador se abrirá y mostrará las gráficas.

> **Nota:** VS Code ejecuta D3.js únicamente dentro de archivos **HTML**, no en archivos `.js` independientes.

## Estructura del código

Cada gráfica requiere su propio contenedor `<div>` con un `id` distinto. D3.js lo localiza con `d3.select("#id")`:

```html
<h2>Noticias por categoría</h2>
<div id="grafico-categoria"></div>

<h2>Noticias por estado</h2>
<div id="grafico-estado"></div>

<h2>Noticias por impacto vial</h2>
<div id="grafico-impacto"></div>
```

La función `dibujarGrafica(selector, datos)` es reutilizable y se invoca una vez por cada gráfica.

Para modificar el tamaño de la gráfica, edite las siguientes constantes:

```js
const ancho = 1024;
const alto = 800;
```

## Tipos de gráficas recomendadas


- Mapa de calor (heatmap), alcaldía × categoría. Mostrar mediante color cuántas noticias hay en cada cruce | Funciona bien con muchas categorías.
- Dona o pastel. Proporciones simples (porcentaje por alcaldía o estado) . Con más de 6 o 7 categorías se dificulta su lectura 
-Barras apiladas (alcaldía × categoría o impacto vial). Responder preguntas como "¿dónde hay más problemas viales altos?" 
- Se implementa con `d3.stack()`

## Solución de problemas

-Error de sintaxis en el código | Falta cerrar una llave `}` | Revisar que cada llave abierta tenga su cierre |
-Las barras no se dibujan | El selector no lleva punto | Usar `.bar` en lugar de `bar` |
-Error al agregar muchas variables al JSON | Llaves, comas o comillas mal colocadas | Validar la estructura del JSON |

## Trabajo pendiente

- [ ] Definir el formato  de datos que utilizará el equipo.

## Notas del autor

- Los videos de D3.js disponibles tenían más de 10 años de antigüedad, por lo que se utilizó Claude Code como apoyo para el aprendizaje.
- El autor se encuentra repasando HTML durante el desarrollo.
## Estructura del código

Cada gráfica requiere su propio contenedor `<div>` con un `id` distinto. D3.js lo localiza con `d3.select("#id")`:

```html
<h2>Noticias por categoría</h2>
<div id="grafico-categoria"></div>

<h2>Noticias por estado</h2>
<div id="grafico-estado"></div>

<h2>Noticias por impacto vial</h2>
<div id="grafico-impacto"></div>
```

La función `dibujarGrafica(selector, datos)` es reutilizable y se invoca una vez por cada gráfica.

Para modificar el tamaño de la gráfica, edite las siguientes constantes:

```js
const ancho = 1024;
const alto = 800;
```

## Tipos de gráficas recomendadas

| Gráfica | Uso recomendado | Observación |

| Mapa de calor (heatmap), alcaldía × categoría | Mostrar mediante color cuántas noticias hay en cada cruce | Funciona bien con muchas categorías |
| Dona o pastel | Proporciones simples (porcentaje por alcaldía o estado) | Con más de 6 o 7 categorías se dificulta su lectura |
| Barras apiladas (alcaldía × categoría o impacto vial) | Responder preguntas como "¿dónde hay más problemas viales altos?" | Se implementa con `d3.stack()` |

## Solución de problemas

| Síntoma | Causa probable | Solución |

| Error de sintaxis en el código | Falta cerrar una llave `}` | Revisar que cada llave abierta tenga su cierre |
| Las barras no se dibujan | El selector no lleva punto | Usar `.bar` en lugar de `bar` |
| Error al agregar muchas variables al JSON | Llaves, comas o comillas mal colocadas | Validar la estructura del JSON |

## Trabajo pendiente

- [ ] Definir el formato (contrato) de datos que utilizará el equipo.

## Notas del autor

- Los videos de D3.js disponibles tenían más de 10 años de antigüedad, por lo que se utilizó Claude Code como apoyo para el aprendizaje.
- El autor se encuentra repasando HTML durante el desarrollo.

## Autor

**Jesus Luna**
