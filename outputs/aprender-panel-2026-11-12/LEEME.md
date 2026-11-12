# Aprender por provincia y sector, 2016–2025

La base reúne las nueve ediciones disponibles en los archivos compartidos. Fecha de elaboración: 12 de noviembre de 2026.

## Contenido

- **Excel**: `Aprender_provincia_sector_2016_2025.xlsx`. Hojas Panel provincial, Muestra nacional 2019, Cobertura, Método y Excepciones. Panel provincial tiene filtros en los encabezados.
- **Base para análisis**: `panel_provincial.csv`, una fila por provincia, año, nivel, grado agrupado y sector. 720 filas. Las materias están en columnas con sus nombres originales. Contiene 1.484 promedios válidos y cuatro resultados ausentes de Chubut 2019.
- **Muestra nacional**: `muestra_nacional_2019.csv`, dos filas por sector, con TEN y TEC como columnas (cuatro promedios nacionales).
- **Cobertura de archivos**: `cobertura.csv`, 16 archivos con 5.780.033 registros en total. Este total no representa estudiantes únicos entre años.
- **Excepciones**: `sector_sin_clasificar.csv`, dos filas que resumen los 29 registros de 2016 con código de sector 3. No se asignan a público o privado.
- **Validaciones**: `validacion.csv`, controles de 33 combinaciones de archivo y materia.

## Ediciones incluidas

| Año | Nivel y grado tal como se suministra | Materias | Diseño |
|---|---|---|---|
| 2016 | Primaria 3.º | Lengua, Matemática | Muestral |
| 2016 | Primaria 6.º | Lengua, Matemática | Censal |
| 2016 | Secundaria 2.º/3.º | Lengua, Matemática | Muestral |
| 2016 | Secundaria 5.º/6.º | Lengua, Matemática, Ciencias Naturales, Ciencias Sociales | Censal |
| 2017 | Primaria 6.º | Ciencias Naturales, Ciencias Sociales | Censal |
| 2017 | Secundaria 5.º/6.º | Lengua, Matemática | Censal |
| 2018 | Primaria 6.º | Lengua, Matemática | Censal |
| 2019 | Secundaria 5.º/6.º | Lengua, Matemática | Censal |
| 2019 | Secundaria 5.º/6.º | Ciencias Naturales, Educación Ciudadana | Muestral, solo resultados nacionales por sector |
| 2021 | Primaria 6.º | Lengua, Matemática | Censal |
| 2022 | Primaria 6.º | Lengua, Matemática | Muestral |
| 2022 | Secundaria 5.º/6.º | Lengua, Matemática | Censal |
| 2023 | Primaria 6.º | Lengua, Matemática | Censal |
| 2024 | Primaria 3.º | Lectura (variable original de prefijo l) | Muestral |
| 2024 | Secundaria 5.º/6.º | Lengua, Matemática | Censal |
| 2025 | Primaria 6.º | Lengua, Matemática | Censal |

La cobertura se identifica a partir de los archivos efectivamente disponibles. No se crean filas para grados o materias que no fueron evaluados en una edición. Los grados agrupados de secundaria se conservan, sin deducir un grado exacto a partir de edad o de preguntas de contexto. Las cuatro celdas de Chubut 2019, Lengua/Matemática por sector, se mantienen sin estimación.

## Cálculo y uso

El promedio representa estudiantes del grupo: suma de puntajes multiplicados por el ponderador de la materia, dividida por la suma de esos ponderadores. Se usan puntajes numéricos y pesos positivos. Los espacios de 2025 se interpretan como faltantes y las comas como separador decimal. No se usa el ponderador del cuestionario general. Para 2019 se toman TEL, TEM, TEN y TEC; en 2024 secundaria y 2025 se toman ponderL y ponderM. Cada fila conserva el archivo fuente.

### Nombres originales y variables calculadas

- `lpuntaje`, `mpuntaje`, `cnpuntaje`, `cspuntaje`, `TEL`, `TEM`, `TEN`, `TEC`: nombres originales, cuyo contenido aquí es el **promedio ponderado del grupo**, no el puntaje individual. Las columnas no disponibles en una edición quedan vacías, sin fusionar TEL con lpuntaje, por ejemplo.
- `sector`: códigos originales 1/2/3, o texto Estatal/Privado en secundaria 2022. `sector_etiqueta` es una etiqueta derivada.
- `cod_provincia` y `jurisdiccion`: se conserva el nombre que usa cada archivo. Los códigos se guardan como texto de dos dígitos. `provincia` y `provincia_codigo` son variables de enlace derivadas.
- `n_lpuntaje`, etc.: número de estudiantes con puntaje válido. `n_escuelas_lpuntaje`, etc.: escuelas con esos puntajes.
- `ldesemp_1_prop`, etc.: proporciones derivadas, identificadas con la variable original de desempeño y su código. No se calcula una media de códigos ordinales.
- `suma_lpondera_puntaje`, etc.: denominador del promedio entre puntajes válidos. `suma_lpuntaje_por_lpondera`, etc.: numerador. `suma_lpondera_desempeno`, etc.: denominador independiente de las proporciones de desempeño.
- Año, nivel, grado y operativo proceden del archivo. Los nombres de conteos, proporciones y sumas son nuevos porque esas variables agregadas no existen en el microdato original.

Las proporciones por código de desempeño usan los registros con desempeño válido y peso positivo, independientemente de la disponibilidad de puntaje. Esto importa en lectura 2024: 2.305 registros tienen desempeño válido pero no puntaje numérico. Se guardan ambos denominadores por separado. Las proporciones están entre 0 y 1 (no entre 0 y 100). Códigos no aplicables quedan vacíos.

Se conservan los códigos originales 1–4 de las pruebas tradicionales y 0–5 de alfabetización 2024. Antes de atribuir etiquetas o comparar categorías, consultar el diccionario de la edición. La prueba de lectura 2024 se mantiene como materia distinta y no se declara comparable directamente con Lengua 3.º de 2016.

Los conteos son registros y escuelas observadas con resultados válidos; no son tasas de participación. La suma de pesos se presenta como denominador del promedio, no como matrícula oficial. Los registros con sector 3 permanecen en un archivo separado y sus resultados no entran en las estimaciones Estatal/Privado.

No se estimaron errores estándar, intervalos de confianza ni significación estadística: hace falta incorporar el diseño muestral de cada edición. Para muestras provinciales debe confirmarse el dominio provincia-sector y su precisión. La muestra de 2019 se mantiene solo a escala nacional por sector, de acuerdo con el documento metodológico oficial. Las diferencias público/privado son descriptivas y no ajustan por composición socioeconómica.

Reunir resultados no certifica por sí solo la comparabilidad temporal de todas las ediciones. Hay que revisar el anclaje de la escala para cada grado, materia y edición antes de estimar tendencias. El panel sigue grupos provinciales, no a los mismos estudiantes o escuelas.

## Verificación realizada

Se verificaron claves de estudiante sin duplicados dentro de cada archivo (ID de escuela, sección e identificador de alumno), provincias reconocidas, pesos positivos, códigos de desempeño permitidos, medias dentro del rango observado, proporciones que suman uno y reconciliación de registros, conteos válidos, pesos y numeradores ponderados contra los originales. No se eliminaron registros duplicados de forma automática. No se combinaron archivos censales y muestrales de una misma materia.

## Fuentes

Evaluación Aprender, archivos de estudiantes compartidos para API-209. El detalle de archivos y vínculos está en `educ-argentina/data/download_manifest.csv` y en `archivo_fuente` de la base.

- [Documento metodológico oficial](https://www.argentina.gob.ar/sites/default/files/documento_metodologico_aprender_4.pdf): ponderación por disciplina, anclaje y alcance de la muestra 2019.
- [Informe de alfabetización 2024](https://www.argentina.gob.ar/sites/default/files/aprender_alfabetizacion2024.pdf): evaluación de lectura y seis niveles de desempeño.

## Abrir en RStudio

Desde el proyecto `educ-argentina`, ejecutar `source("R/03_load_aprender_panel.R")` y luego `View(aprender_panel)`. Los CSV también se guardaron en `data/processed/`. Para reconstruirlos, ejecutar `scripts/build_aprender_panel.py` con Python, pandas y numpy. Los originales no se modifican.
