# Proyecto de Inteligencia Artificial — Clasificación del Riesgo de Salud Materna

- **Dataset:** Maternal Health Risk (UCI Machine Learning Repository, ID 863)
- **Fuente:** <https://archive.ics.uci.edu/dataset/863/maternal+health+risk> — Marzia Ahmed, Daffodil International University (CC BY 4.0)
- **Herramienta:** Weka 3.8
- **Tipo de tarea:** Clasificación supervisada multiclase (3 clases)
- **Variable objetivo:** `RiskLevel` → `low risk` / `mid risk` / `high risk`

![[Pasted image 20260926172535.png]]

---

## Índice

1. [Resumen del proyecto](#1-resumen-del-proyecto)
2. [¿En qué consiste el proyecto?](#2-en-qué-consiste-el-proyecto)
3. [¿Por qué se escogió este dataset?](#3-por-qué-se-escogió-este-dataset)
4. [Descripción del dataset](#4-descripción-del-dataset)
5. [Antecedentes, marco teórico e información complementaria](#5-antecedentes-marco-teórico-e-información-complementaria)
6. [Metodología: preparación de los datos](#6-metodología-preparación-de-los-datos)
7. [Metodología: cómo se hizo el entrenamiento](#7-metodología-cómo-se-hizo-el-entrenamiento)
8. [Resultados](#8-resultados)
9. [Análisis y discusión de resultados](#9-análisis-y-discusión-de-resultados)
10. [Conclusiones](#10-conclusiones)
11. [Referencias](#11-referencias)

---

## 1. Resumen del proyecto

Este proyecto consiste en construir y comparar modelos de aprendizaje supervisado capaces de
**predecir el nivel de riesgo de salud materna durante el embarazo** a partir de seis
medidas clínicas elementales: edad, presión arterial sistólica, presión arterial diastólica,
glucosa en sangre, temperatura corporal y frecuencia cardíaca.

El dataset se obtuvo del **UCI Machine Learning Repository** (ID 863, donado por Marzia Ahmed,
Daffodil International University, bajo licencia CC BY 4.0) y fue recolectado en hospitales,
clínicas comunitarias y centros de atención materna de zonas rurales de Bangladesh. Esto le da
al problema un valor social directo: la mortalidad materna es una de las metas de los Objetivos
de Desarrollo Sostenible de la ONU (Naciones Unidas, 2024), y en las zonas rurales los
recursos humanos especializados son escasos.

Todo el proceso experimental —carga, particionado, entrenamiento y evaluación— se realizó en
**Weka**, usando el entorno de clasificación de Weka con la configuración de métricas
`%a` (accuracy), `%error`, `1kappa` y el tiempo de extracción, que es el formato exigido
para la entrega.

---

## 2. ¿En qué consiste el proyecto?

### 2.1 Problema

Durante el embarazo, una mujer puede presentar complicaciones que pueden evolucionar rápidamente y que son
evitables si se detectan a tiempo (hipertensión, diabetes gestacional, fiebre,
taquicardia) (Organización Mundial de la Salud, 2025). En las zonas rurales de Bangladesh, el
personal médico especializado no está siempre disponible, y la supervisión médica puede ocurrir
únicamente cada varias semanas.

La pregunta de investigación es:

> **¿Es posible clasificar automáticamente el nivel de riesgo de una embarazada
> (`low risk`, `mid risk`, `high risk`) a partir de seis constantes vitales de bajo costo,
> registradas en una consulta de rutina?**

### 2.2 Solución propuesta

Un clasificador supervisado que, dada la medición de las seis variables, asigna una de las
tres categorías de riesgo:

![[Pasted image 20260926171652.png]]

### 2.3 Alcance del experimento

Se entrenan y comparan **cuatro modelos de clasificación** de la librería de Weka, sobre el mismo dataset y con la misma
partición, de modo que las diferencias en rendimiento sean atribuibles únicamente al
algoritmo.

| # | Algoritmo | Familia | Justificación de su inclusión |
|---|-----------|---------|------------------------------|
| 1 | **IBk** (k-NN, k = 1) | Basado en instancias | Categorías ordenadas y datos tabulares pequeños; representa el mínimo esfuerzo de cómputo. |
| 2 | **SVM** | Margen máximo | Funciona bien con atributos numéricos y pocas muestras; modela fronteras de decisión no lineales. En Weka se implementa en la clase `SMO`. |
| 3 | **MultilayerPerceptron** (MLP) | Red neuronal | Aprende interacciones no lineales entre constantes vitales. |
| 4 | **NaiveBayes** | Probabilístico | Hipótesis de independencia; línea base clásica y muy rápida. |

---

## 3. ¿Por qué se escogió este dataset?

Se escogió por seis razones concretas:

1. **Relevancia social y alineación con los ODS.** La salud materna es el eje de la meta
   3.1 de los Objetivos de Desarrollo Sostenible: *reducir la tasa de mortalidad materna
   global a menos de 70 muertes por cada 100,000/SCS* (Naciones Unidas, 2024). Un modelo
   predictivo sobre esta variable tiene impacto directo en esa meta.

2. **Tamaño de muestra apropiado para la carga de un examen.** Con 1,014 registros, el dataset
   es suficientemente grande para obtener métricas confiables y, al mismo tiempo, lo bastante
   pequeño para entrenar y evaluar varios algoritmos rápidamente en Weka.

3. **Problema de clasificación multiclase real (3 clases).** No se limita a binario
   (`sí/no`), lo que obliga a evaluar de manera más rigurosa y hace el análisis más
   interesante que un problema de dos clases.

4. **Todas las variables son numéricas y de bajo costo de medición.** Age, las dos presiones,
   la glucosa, la temperatura y la frecuencia cardíaca se obtienen con un equipo básico de
   consulta. Esto hace el modelo **aplicable en el contexto rural** donde nació el dataset:
   no requiere laboratorio, ni imágenes, ni historia clínica completa.

5. **Atributos fisiológicamente interpretables.** A diferencia de un problema de imágenes o de
   texto, cada variable tiene un significado médico directo y conocido. Si un médico discrepa
   con la predicción, puede identificar *qué* constante vital está determinando la decisión.
   La **interpretabilidad** es un criterio de evaluación en salud, no un lujo.

6. **Es un dataset público, pequeño y limpio.** No tiene valores faltantes, lo que elimina la
   fase de imputación y permite concentrar el esfuerzo en la comparación de modelos.

---

## 4. Descripción del dataset

### 4.1 Ficha técnica

| Campo | Valor |
|-------|-------|
| Nombre | Maternal Health Risk Data Set |
| Repositorio | UCI Machine Learning Repository |
| URL de origen | <https://archive.ics.uci.edu/dataset/863/maternal+health+risk> |
| ID / DOI | 863 / 10.24432/C5DP5D |
| Tipo | Multivariante, datos reales y enteros |
| Área | Salud y Medicina |
| Tarea asociada | Clasificación |
| Instancias | 1,014 registros de datos (la ficha de UCI declara 1,013; el archivo CSV real contiene 1,014 filas) |
| Características | 6 atributos predictores + 1 variable objetivo |
| Valores faltantes | No |
| Licencia | Creative Commons Attribution 4.0 International (CC BY 4.0) |
| Fecha de donación | 14 de agosto de 2023 |
| Origen | Hospitales, clínicas comunitarias y atención materna en zonas rurales de Bangladesh |
| Autora y fuente | Marzia Ahmed — Daffodil International University |

> **Crédito y atribución de la fuente.** Los datos utilizados en este proyecto proceden del
> *Maternal Health Risk Data Set* publicado en el **UCI Machine Learning Repository**
> (ID 863), creado y donado por **Marzia Ahmed** (Daffodil International University).
> El archivo `Maternal Health Risk Data Set.csv` es una copia local sin modificaciones de
> dicho dataset. Al estar bajo licencia **CC BY 4.0**, reutilizarlo exige mantener esta
> atribución, que se completa en la sección 12 de Referencias.

### 4.2 Estructura del archivo CSV original

El archivo `Maternal Health Risk Data Set.csv` contiene una primera línea de encabezado y
luego una fila por cada embarazada registrada:

```csv
Age,SystolicBP,DiastolicBP,BS,BodyTemp,HeartRate,RiskLevel
25,130,80,15,98,86,high risk
35,140,90,13,98,70,high risk
29,90,70,8,100,80,high risk
...
```

### 4.3 Diccionario de variables

| Variable | Rol | Tipo | Unidad | Descripción |
|----------|-----|------|--------|-------------|
| `Age` | Feature | Entero | años | Edad de la mujer en el momento del embarazo. |
| `SystolicBP` | Feature | Entero | mmHg | Valor superior de la presión arterial; atributo significativo durante el embarazo. |
| `DiastolicBP` | Feature | Entero | mmHg | Valor inferior de la presión arterial; atributo significativo durante el embarazo. |
| `BS` | Feature | Real | mmol/L | Nivel de glucosa en sangre como concentración molar. |
| `BodyTemp` | Feature | Entero | °F | Temperatura corporal. |
| `HeartRate` | Feature | Entero | bpm | Frecuencia cardíaca en reposo; un valor normal se sitúa alrededor de 60–100 bpm. |
| `RiskLevel` | **Target** | Categórica | — | Nivel de intensidad de riesgo predicho durante el embarazo, a partir de las variables anteriores. |

### 4.4 Variable objetivo: las tres clases

| Clase       | Significado       | En Weka  | Instancias | % del total |
| ----------- | ----------------- | -------- | ---------- | ----------- |
| `low risk`  | Riesgo bajo       | `low`    | 406        | 40.04 %     |
| `mid risk`  | Riesgo intermedio | `mid`    | 336        | 33.14 %     |
| `high risk` | Riesgo alto       | `high`   | 272        | 26.82 %     |
| **Total**   |                   |          | **1,014**  | **100 %**   |
![[Pasted image 20260926143528.png]]

> La columna "En Weka" indica el nombre con el que aparecerán las clases dentro de Weka: el
> archivo `.arff` las abrevia porque Weka no admite espacios en las etiquetas nominales
> (ver sección 6.2). El significado de cada clase es el mismo.

> Las clases están **balanceadas de forma natural** (proporción 40/33/27).

---

## 5. Antecedentes, marco teórico e información complementaria

### 5.1 Antecedentes: qué se ha hecho con esta base de datos

Esta base de datos se ha reutilizado en varios trabajos de aprendizaje automático, casi siempre
para comparar el desempeño de clasificadores sobre el nivel de riesgo materno:

- **Ahmed et al. (2020)** publicaron el artículo que acompaña al dataset, justifica las seis
  variables como factores de riesgo y describe el proceso de recolección de los datos.
- **Togunwa, Babatunde y Abdullah (2023)** combinaron una red neuronal artificial con Random
  Forest (modelo híbrido) y alcanzaron 94.88 % de *accuracy*; en su tabla comparativa, KNN (65.3 %),
  SVM (55.5 %) y Naive Bayes (59.3 %) rindieron por debajo de los métodos de conjunto.
- **Venkatesh, Jha, Kazmi y Zaidi (2024)** compararon XGBoost, Random Forest, KNN, SVM y
  regresión logística con *accuracies* de 58.7 % a 82.6 %, e identificaron la glucosa en sangre
  y la presión arterial sistólica como las variables más relevantes.

Lo que aporta este trabajo es comparar los cuatro algoritmos clásicos evaluados aquí
(KNN, SVM, Naive Bayes y RNA multicapa) bajo un mismo protocolo de partición 70/30 y con las
métricas de Weka.

### 5.2 Marco teórico: KNN (IBk)

Asigna a una instancia la clase mayoritaria entre sus `k` vecinos más próximos en el espacio de
atributos, usando una distancia (en este trabajo, euclidiana). No construye un modelo explícito:
memoriza el conjunto de entrenamiento y decide en el momento de la consulta. Con `k = 1` la
frontera de decisión se ajusta exactamente a los datos de entrenamiento, por lo que es sensible
al ruido y a los registros duplicados (Witten et al., 2016).

### 5.3 Marco teórico: SVM

Busca la frontera que maximiza el margen entre las clases; los puntos que la definen son los
vectores de soporte. Con kernel no lineal (polinomial o RBF) modela fronteras curvas sin
transformar explícitamente los datos. Es potente con muestras pequeñas, aunque su costo de
entrenamiento crece con el número de instancias (Witten et al., 2016).

### 5.4 Marco teórico: Naive Bayes

Aplica la regla de Bayes suponiendo que los atributos son independientes entre sí dada la clase;
la predicción resulta del producto de las probabilidades condicionales de cada atributo. Es muy
rápido y sirve como línea base, aunque la independencia es una simplificación que rara vez se
cumple (Witten et al., 2016).

### 5.5 Marco teórico: RNA multicapa (MultilayerPerceptron)

Organiza neuronas en capas: una capa de entrada con las seis constantes vitales, una o más capas
ocultas que aplican activaciones no lineales y una capa de salida con una neurona por clase. Los
pesos se ajustan por retropropagación y descenso del gradiente. Su capacidad de modelar
interacciones no lineales crece con el número de neuronas, pero con pocas instancias tiende al
sobreajuste (Witten et al., 2016).

### 5.6 Por qué importan estas constantes vitales

La elección de atributos no es arbitraria; cada uno tiene evidencia fisiológica
asociada a complicaciones del embarazo:

- **Presión arterial (sistólica y diastólica):** su elevación sostenida es el síntoma
  precursor de la hipertensión gestacional y de la preeclampsia, una de las principales causas
  de muerte materna prevenible.
- **Glucosa en sangre (BS):** valores elevados sugieren diabetes gestacional, asociada a
  macrosomía fetal, parto prematuro y complicaciones neonatales.
- **Temperatura corporal (BodyTemp):** la fiebre durante el embarazo puede indicar infección,
  que es una causa importante de morbilidad materna en contextos de baja cobertura sanitaria.
- **Frecuencia cardíaca (HeartRate):** una taquicardia persistente puede ser el primer signo
  de anemia, sepsis o compromiso cardiovascular.
- **Edad (Age):** las edades extremas (muy jóvenes o mayores de 35 años) se asocian con
  mayor riesgo obstétrico (Ahmed et al., 2020; Organización Mundial de la Salud, 2025).

![[Pasted image 20260926171254.png]]

### 5.7 Contexto de la salud materna mundial

Según la Organización Mundial de la Salud (2025), la mayoría de las muertes maternas son
**prevenibles** y se asocian a tres condiciones: (a) ausencia de atención sanitaria calificada
durante el embarazo y el parto, (b) uso de anticoncepción insuficiente y (c) acceso limitado a
servicios de salud sexual y reproductiva. Este proyecto aborda el primer punto: **brindar una
alerta objetiva y automatizada a partir de mediciones poco invasivas**, incluso cuando
no hay un profesional disponible en el momento.

### 5.8 Implicaciones éticas

- El dataset es **anónimo**: no contiene identificadores personales, lo que reduce riesgos de
  re-identificación.
- El modelo debe usarse como **apoyo a la decisión profesional**, nunca como sustituto de un
  diagnóstico médico.
- La licencia CC BY 4.0 obliga a dar crédito a la autoría (Ahmed, 2020); este documento lo
  hace en la sección de Referencias.

---

## 6. Metodología: preparación de los datos

### 6.1 Carga del dataset en Weka

> **Vía recomendada:** abrir directamente `data/maternal_health_risk_train.arff` con el botón
> **Open Data…** de la pestaña *Preprocess*. Al ser ARFF, Weka reconoce el esquema y la clase
> sin pedir ningún dato de formato. La carga manual del CSV que se describe a continuación
> también es válida, pero es más lenta y propensa a errores de delimitador.

El dataset se cargó en Weka mediante el botón **Open Data…** o el **Data Explorer**, seleccionando
el archivo `Maternal Health Risk Data Set.csv`. Weka pide confirmar el formato CSV:

- *Relation name*: `maternal_health_risk`
- *Attribute-Header line*: **1** (primera línea)
- *Attribute delimiter*: `,` (coma)
- *Quote character*: `"` (comillas dobles)
- *Attribute type*: **numeric** para las 6 features
- *Class index*: `RiskLevel` (última columna → `>>` en el visor de atributos)

> **Importante:** Weka detecta los valores como `numeric` para las columnas de features. Al
> revisar el panel **Attribute** se debe confirmar que `RiskLevel` quedó como `nominal`
> y que es el **class attribute** (botón derecho → *Set class index* si es necesario).

![[Pasted image 20260926172012.png|700]]

![[Pasted image 20260926172021.png|700]]

### 6.2 Generación de los subconjuntos 70/30

Para poder entrenar y después **validar** el modelo con datos que nunca vio durante el
aprendizaje, se dividió el dataset en dos subconjuntos:

- **Entrenamiento (`_train`): 70 % de los datos → 709 registros**
- **Prueba (`_test`): 30 % de los datos → 305 registros**

La división se realizó con un **script de Python (`scripts/split_dataset.py`)** usando
`train_test_split` de *scikit-learn* con dos garantías importantes:

1. **Aleatoriedad controlada:** `random_state = 42`, para que el resultado sea **reproducible**
   (cualquiera puede regenerar exactamente los mismos archivos).
2. **Estratificación por clase:** `stratify = RiskLevel`, de modo que la proporción de
   `low / mid / high risk` se mantiene casi idéntica en ambos subconjuntos.

Se generaron **dos formatos** de cada archivo, ambos importables en Weka:

| Archivo | Formato | Instancias | ¿Para qué se usa? |
|---------|---------|-----------|-------------------|
| `data/maternal_health_risk_train.dat` | CSV con encabezado | 709 | Carga directa con el formato CSV de Weka |
| `data/maternal_health_risk_test.dat` | CSV con encabezado | 305 | Carga directa con el formato CSV de Weka |
| `data/maternal_health_risk_train.arff` | **ARFF nativo** (declarado `@attribute`/`@data`) | 709 | **Recomendado**: Weka detecta el esquema solo, sin configuración manual |
| `data/maternal_health_risk_test.arff` | **ARFF nativo** | 305 | **Recomendado** para el conjunto de prueba |

Cabecera del `.arff` generado:

```arff
% Maternal Health Risk (UCI, id=863)
% Ahmed, M. (2020). Maternal Health Risk [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5DP5D
% Licencia CC BY 4.0. Particion generada por particionado estratificado 70/30 (random_state=42).
% Clases abreviadas porque Weka no admite espacios en etiquetas nominales:
%   low = low risk (riesgo bajo) | mid = mid risk (riesgo medio) | high = high risk (riesgo alto)
@relation maternal_health_risk

@attribute Age numeric
@attribute SystolicBP numeric
@attribute DiastolicBP numeric
@attribute BS numeric
@attribute BodyTemp numeric
@attribute HeartRate numeric
@attribute RiskLevel {low, mid, high}

@data
25,130,80,15,98,86,high
...
```

> **Detalle importante:** en el `.arff` las clases aparecen abreviadas como `low`, `mid` y `high`
> en lugar de `low risk`, `mid risk` y `high risk`. Weka **no admite espacios dentro de las
> etiquetas de un atributo nominal**: al leer `{low risk, mid risk, high risk}` las separa por
> espacios, interpreta `risk` como una etiqueta repetida y aborta con
> `A nominal attribute (RiskLevel) cannot have duplicate labels (risk)`. Los archivos `.dat`
> (CSV) sí conservan los nombres originales completos.

> **Ventaja de ARFF:** es el formato nativo de Weka, con los tipos de dato declarados
> explícitamente. Al abrirlo, el `class attribute` ya queda correctamente configurado y no
> hay riesgo de errores de parseo por el delimitador.

![[Pasted image 20260926172309.png]]

### 6.3 Verificación de la distribución de los subconjuntos

Un punto crítico de un particionado 70/30 es que **ambos subconjuntos sigan siendo
representativos**. Si, por azar, el 30 % de prueba tuviera casi solo ejemplos de `high risk`,
el modelo se evaluaría con un criterio injusto. Por eso la script verifica automáticamente que
la estratificación se cumpla (ver `data/distribucion_split.txt`):

**Comparativo de distribución de clases**

| Clase | Original (1014) | Train (70 %) | % train | Test (30 %) | % test | Desviación |
|-------|-----------------|--------------|---------|-------------|--------|------------|
| `low risk` | 406 | 284 | 40.06 % | 122 | 40.00 % | 0.04 p.p. |
| `mid risk` | 336 | 235 | 33.15 % | 101 | 33.11 % | 0.02 p.p. |
| `high risk` | 272 | 190 | 26.80 % | 82 | 26.89 % | 0.06 p.p. |

**Resultado de la verificación:** la desviación máxima por clase es de **0.06 puntos
porcentuales**, muy por debajo del umbral de 1.00 p.p. definido en la script. **La
distribución está correctamente balanceada.**

Además se comparó la estadística descriptiva de cada variable en ambos conjuntos, confirmando
que train y test son equivalentes también en las variables predictoras:

| Variable | Media train | Media test | Mín. train | Mín. test | Máx. train | Máx. test |
|----------|-------------|------------|------------|------------|------------|------------|
| `Age` | 29.88 | 29.86 | 10 | 12 | 70 | 66 |
| `SystolicBP` | 113.23 | 113.13 | 70 | 70 | 160 | 160 |
| `DiastolicBP` | 76.47 | 76.45 | 49 | 49 | 100 | 100 |
| `BS` | 8.74 | 8.69 | 6 | 6 | 19 | 19 |
| `BodyTemp` | 98.70 | 98.58 | 98 | 98 | 103 | 103 |
| `HeartRate` | 74.55 | 73.71 | 7 | 60 | 90 | 90 |

![[Pasted image 20260926172758.png]]
**de distribución de clases de original, train y test, con las desviaciones.]**

![[Pasted image 20260926172843.png]]

![[Pasted image 20260926172857.png]]
**con el histograma de `RiskLevel` y el panel *Attribute* mostrando los valores mínimos y máximos.]**

### 6.4 Observaciones sobre la calidad de los datos

Durante la inspección se detectaron las siguientes particularidades del dataset original. **Se
decidió conservarlas sin modificar** para no alterar la fuente ni invalidar la comparabilidad
con la literatura, pero se documentan aquí como parte del análisis:

- **Sin valores faltantes:** no hay `null`, `NaN` ni `?` en ninguna celda. No se requiere imputación.
- **Alta repetición de registros:** 562 filas son duplicados exactos de otra fila
  (mismos 6 features y misma clase). Esto es esperable: el equipo de medición registraba
  lecturas repetidas cuando la visita de la paciente no cambiaba. Como consecuencia, **166 registros idénticos aparecen simultáneamente en train y en test**. En modelos de distancia (como IBk) esto puede dar una ventaja artificial, porque la instancia "gemela" está memorizada en el conjunto de entrenamiento. Es una limitación conocida de este dataset y se discute en la sección 10.
- **Valores atípicos:** 2 registros presentan `HeartRate = 7 bpm`, un valor fisiológicamente
  improbable (probablemente un error de captura de un valor 70–77). Ambos pertenecen a la clase `low risk`.

### 6.5 Preprocesamiento en Weka (filtros)

Aunque no se requiere imputación, se aplicó un **preprocesamiento mínimo dentro de Weka** con
la pestaña *Preprocess*, usando el filtro **`Normalize` (rango −1 a 1) sobre cada atributo
numérico**, seguido del filtro **`ClassBalancer`** para preservar el balance de clases:

![[Pasted image 20260926173443.png|410]]

**Parámetros aplicados.** `Normalize` transforma `x' = (x − min) / (max − min) × S + T`, por lo que la salida queda en `[T, T + S]`. Los valores por defecto (`-S 1.0 -T 0.0`) dan el rango [0, 1]; para
obtener [−1, 1] se configuró **`-S 2.0 -T -1.0`**, que es lo que se usó aquí.

**La normalización se ajusta solo con el entrenamiento.** El filtro se aplica sobre
`maternal_health_risk_train.arff` en *Preprocess*, y `maternal_health_risk_test.arff` se carga
después en *Classifier* como **Supervised test set** (*Test options* → *More options*). Weka
transforma ese conjunto con los mínimos y máximos ya calculados en el entrenamiento, no con los
suyos. Normalizar el test por separado, o pre-normalizar el archivo en disco, hace que el modelo
reciba datos en una escala distinta a la que aprendió y filtra estadísticas del propio conjunto de
prueba: con `IBk (k=1)` el accuracy cae de **82.95 %** a **69.51 %**, y a **34.10 %** si el test se
deja sin normalizar. En Weka 3.8.7 la separación entre entrenamiento y prueba no depende de ninguna opción del filtro, sino de la carga en dos archivos distintos.

**Prueba de la decisión.** Se compararon los cuatro clasificadores con y sin normalización sobre la
misma partición:

| Algoritmo | Normalizado | Sin normalizar | Diferencia |
|-----------|-------------|----------------|------------|
| `IBk` (k = 1) | 82.95 % (253) | 82.62 % (252) | +0.33 p.p. |
| `SMO` (SVM) | 62.62 % (191) | 62.62 % (191) | 0.00 p.p. |
| `MultilayerPerceptron` | 67.54 % (206) | 67.54 % (206) | 0.00 p.p. |
| `NaiveBayes` | 61.31 % (187) | 59.34 % (181) | +1.97 p.p. |

Normalizar nunca empeora el resultado, pero el efecto es pequeño por dos razones. Primero, `SMO`
(opción `-N`, por defecto *normalize*) y `MultilayerPerceptron` (opción `-I`, que solo desactiva la
normalización interna si se marca) **normalizan por dentro**, así que el filtro externo les resulta
redundante. Segundo, las seis variables ya viven en rangos estrechos y comparables (presión
70–160, glucosa 6–19, temperatura 98–102), que es justamente el problema que la normalización suele resolver; la diferencia de una sola instancia en `IBk` es ruido estadístico. Se conserva la
normalización porque es el criterio correcto y verificable, y porque es lo único que mejora a los dos
clasificadores que no la aplican internamente (`IBk` y `NaiveBayes`).

> **Advertencia sobre el *percentage split*.** En la tabla de entrenamiento (sección 7.1) se usa
> *Percentage split 70 %* dentro de `train.arff`, de modo que los min/max provienen de las 709
> instancias y no solo de las 496 resultantes: es una fuga leve que afecta únicamente a esa tabla
> de diagnóstico. La validación reportada sale de `test.arff` con el mecanismo limpio descrito
> arriba.

El contraste entre el diseño aplicado y el diseño que habría que evitar:

![[Pasted image 20260926173717.png]]

![[Pasted image 20260926174338.png]]

## 7. Metodología: cómo se hizo el entrenamiento

### 7.1 Protocolo experimental

Se siguió un protocolo idéntico para los cuatro algoritmos, de modo que las diferencias en las
métricas dependan **solo del clasificador**:

1. **Datos de entrenamiento:** `maternal_health_risk_train.arff` (709 instancias).
2. **Datos de validación/prueba:** `maternal_health_risk_test.arff` (305 instancias).
3. **Modo de evaluación:** *Percentage split* = **70 %** *(repartición interna por defecto de
   Weka para obtener la tabla de entrenamiento)* — se deja el valor por defecto de Weka para
   que la tabla de entrenamiento sea directamente comparable con la de Iris.
4. **Métricas registradas:** *Correctly Classified Instances* (`%a`), *Incorrectly Classified
   Instances* (`%error`), *Kappa statistic* (`1kappa`) y *Time taken to build model*.
5. **Semilla:** *Random number seed* = **42**, para reproducibilidad.
6. **Predicción:** se activa **"More options" → "Output predictions"** para poder guardar el
   detalle de aciertos y errores instancia por instancia y luego calcular métricas adicionales
   (matriz de confusión, precisión, exhaustividad).

![[Pasted image 20260926174639.png]]

### 7.2 Configuración de cada clasificador

| Algoritmo | Ruta en Weka | Parámetros usados | Motivo de la configuración |
|-----------|--------------|------------------|----------------------------|
| **IBk** | `Classifiers → Instance Based → IBk` | *KNN* = **1**, *Distance function* = Euclidean, distancia normalizada por Weka | K=1 con 6 atributos numéricos. Un K mayor suavizaría la frontera entre `low` y `mid risk`, que son clases muy próximas en el espacio de atributos. |
| **SVM** | `Classifiers → Functions → SMO` | Kernel = **Polynomial** (grado 2) / RBF, C = 1.0, Epsilon = 1.0e-3, *Optimize* = true | Permite fronteras no lineales con solo 709 muestras. Se probó también la configuración por defecto (lineal) para comparar. |
| **MultilayerPerceptron** | `Classifiers → Functions → MultilayerPerceptron` | 1 capa oculta, **2–5 neuronas**, `learningRate` = 0.1, `momentum` = 0.0, `decay` = false, *Normalize* = true | Arquitectura pequeña y suficiente para 6 entradas; evita el sobreajuste con tan pocas muestras. |
| **NaiveBayes** | `Classifiers → Bayes → NaiveBayes` | Parámetros por defecto (0.01) | Supone independencia entre atributos. Sirve como línea base: si no supera a los demás, la dependencia entre variables es relevante. |

### 7.3 Procedimiento paso a paso (reproducible)

![[Pasted image 20260926174856.png]]

> **Aclaración sobre la "Tabla de Entrenamiento" vs "Tabla de Validación":**
> - La **tabla de entrenamiento** proviene de correr el clasificador en modo *Percentage
>   split* 70 % (train dentro del train). Refleja qué tan bien el modelo **aprendió**.
> - La **tabla de validación (prueba)** proviene de cargar el `.dat/.arff` de prueba como
>   *supervised test set*. Refleja qué tan bien el modelo **generaliza**.
> La brecha entre ambas tablas es la medida más informativa del ejercicio: si una es alta y la
> otra baja, el modelo está **sobreajustado** (memoriza el entrenamiento).

![[Pasted image 20260926175252.png]]

![[Pasted image 20260926175612.png]]

---
## 8. Resultados

> **Configuración realmente ejecutada.** Los resultados de esta sección provienen de ocho
> corridas en Weka 3.8.7 (cuatro algoritmos × dos modos de evaluación) sobre
> `maternal_health_risk_train.arff` (709 instancias) y `maternal_health_risk_test.arff`
> (305 instancias).

### 8.1 Tabla de Entrenamiento (maternal_health_risk_train)

Modo de evaluación: *evaluate on training data* (709 instancias). Mide **ajuste**, es decir, cómo
de bien el modelo se ajusta a los mismos datos con los que se entrenó.

| Algoritmo | Clasificación | No Clase | %a | %error | 1kappa | Tiempo de extracción | Tiempo de prueba |
|---|---|---|---|---|---|---|---|
| IBk (k=1) | 655 | 54 | 92.3836 % | 7.6164 % | 0.8843 | 0 s | 0.02 s |
| SMO (SVM) | 456 | 253 | 64.3159 % | 35.6841 % | 0.4436 | 0.03 s | 0.01 s |
| MultilayerPerceptron | 480 | 229 | 67.701 % | 32.299 % | 0.5028 | 0.34 s | 0 s |
| NaiveBayes | 432 | 277 | 60.9309 % | 39.0691 % | 0.3857 | 0 s | 0.01 s |

![[Pasted image 20260926183147.png]]

![[Pasted image 20260926183200.png]]

![[Pasted image 20260926183208.png]]

![[Pasted image 20260926183216.png]]

> **Cómo se llenó la tabla:** en la pestaña *Classifier* de Weka, la fila
> `Correctly Classified Instances` da la columna **Clasificación** y su porcentaje la columna
> **%a**; la fila `Incorrectly Classified Instances` da **No Clase** y **%error**;
> `Kappa statistic` da **1kappa**; `Time taken to build model` da el **tiempo de extracción**;
> y `Time taken to test model` da el **tiempo de prueba**.

**`IBk` no alcanza el 100 % ni sobre sus propios datos de entrenamiento.** No es un error de
configuración: el dataset contiene **27 grupos de filas con los seis valores idénticos pero
etiquetas de riesgo distintas** (151 instancias de entrenamiento afectadas). Con k=1 el vecino
más cercano está a distancia 0, pero es ambiguo entre duplicados contradictorios, de modo que 54
errores son inevitables. Es decir, **el error de Bayes de este dataset no es cero** y ningún
clasificador puede superarlo.

### 8.2 Tabla de Validación (maternal_health_risk_test)

Modo de evaluación: *user supplied test set* (305 instancias). Mide **generalización**, es decir,
cómo se comporta el modelo en pacientes que no vio durante el entrenamiento.

| Algoritmo | Clasificación | No Clase | %a | %error | 1kappa | Tiempo de extracción | Tiempo de prueba |
|---|---|---|---|---|---|---|---|
| **IBk (k=1)** | **252** | 53 | **82.623 %** | 17.377 % | **0.7356** | 0 s | 0.01 s |
| MultilayerPerceptron | 206 | 99 | 67.541 % | 32.459 % | 0.4977 | 0.28 s | 0 s |
| SMO (SVM) | 191 | 114 | 62.623 % | 37.377 % | 0.4131 | 0.02 s | 0 s |
| NaiveBayes | 181 | 124 | 59.3443 % | 40.6557 % | 0.3587 | 0 s | 0 s |

![[Pasted image 20260926183244.png]]

![[Pasted image 20260926183252.png]]

![[Pasted image 20260926183259.png]]

![[Pasted image 20260926183305.png]]

Las dos tablas comparten modelo: en las ocho corridas el bloque `=== Classifier model ===` de `SMO` y de `MultilayerPerceptron` es idéntico byte a byte entre el modo de entrenamiento y el de validación, lo que confirma que ambas evalúan **el mismo modelo** y solo cambia el conjunto sobre el que se mide.

| Algoritmo |Ajuste (8.1) | Generalización (8.2) | Brecha |
|---|---|---|---|
| IBk (k=1) | 92.38 % | 82.62 % | 9.76 p.p. |
| MultilayerPerceptron | 67.70 % | 67.54 % | 0.16 p.p. |
| SMO (SVM) | 64.32 % | 62.62 % | 1.69 p.p. |
| NaiveBayes | 60.93 % | 59.34 % | 1.59 p.p. |

La lectura de estas brechas es contraintuitiva y conviene explicarla en el análisis: una brecha
grande indicaría sobreajuste, pero aquí **solo `IBk` la presenta** (9.76 p.p.), y es el mejor
modelo. En los otros tres la brecha es mínima porque **no llegan a ajustar bien ni sus propios
datos de entrenamiento**: su problema no es la varianza, sino que el modelo no tiene capacidad
suficiente para expresar la frontera entre `low` y `mid risk`.

### 8.3 Matriz de confusión del mejor modelo

Modelo elegido: **`IBk` (k=1)**, corrida de validación sobre el test set externo (305 instancias).
Columnas = clase predicha, filas = clase real.

| Real \ Predicha | low (riesgo bajo) | mid (riesgo medio) | high (riesgo alto) | Total real |
|-----------------|--------------------|---------------------|---------------------|------------|
| **low (riesgo bajo)** | **100** | 18 | 4 | 122 |
| **mid (riesgo medio)** | 20 | **79** | 2 | 101 |
| **high (riesgo alto)** | 3 | 6 | **73** | 82 |
| **Total predicho** | 123 | 103 | 79 | 305 |

Las 53 instancias mal clasificadas se concentran en la frontera `low` ↔ `mid`: 18 pacientes de
riesgo bajo fueron predichas como `mid` y 20 pacientes de `mid` como `low`. Los errores hacia
`high risk` son mínimos (6 en total desde `low` y `mid`), lo que es coherente con el criterio
clínico de la sección 9.1: es preferible clasificar de más a una paciente grave que dejar pasar
un caso severo.

![[Pasted image 20260926183354.png]]

![[Pasted image 20260926183345.png]]
### 8.4 Métricas complementarias

Valores del bloque *Detailed Accuracy By Class*, fila **Weighted Avg.** de cada corrida de
validación (promedio ponderado por número de instancias):

| Algoritmo | Precision | Exhaustividad | F1 | AUC (ROC Area) |
|-----------|-----------|----------------|-----|----------------|
| **IBk (k=1)** | **0.828** | **0.826** | **0.827** | **0.903** |
| MultilayerPerceptron | 0.682 | 0.675 | 0.667 | 0.816 |
| SMO (SVM) | 0.645 | 0.626 | 0.600 | 0.713 |
| NaiveBayes | 0.583 | 0.593 | 0.545 | 0.782 |

Como en salud materna no todas las clases tienen el mismo costo, el promedio agregado esconde lo
importante. La **exhaustividad por clase** en el conjunto de validación es:

| Algoritmo | low | mid | high |
|-----------|-----|-----|------|
| **IBk (k=1)** | 0.820 | **0.782** | **0.890** |
| MultilayerPerceptron | 0.836 | 0.406 | 0.768 |
| SMO (SVM) | 0.910 | 0.267 | 0.646 |
| NaiveBayes | 0.934 | 0.139 | 0.646 |

**La clase `mid` es el talón de Aquiles de los cuatro modelos.** `NaiveBayes` solo identifica 14 de
los 101 casos `mid` del test (exhaustividad 0.139) y envía 81 de ellos a `low risk`; el `SMO` apenas
llega a 0.267. Solo `IBk` mantiene las tres clases por encima de 0.78. En la práctica esto significa
que con `NaiveBayes`, `SMO` o `MultilayerPerceptron` la mayoría de las pacientes de riesgo
intermedio se clasificarían como de riesgo bajo, que es el error más probable de pasar por alto en
una consulta.

Detalle por clase del modelo elegido (`IBk`, k=1), que es el que se reporta:

| Clase | TP Rate | FP Rate | Precision | Recall | F-Measure | MCC | ROC Area | PRC Area |
|-------|---------|---------|-----------|--------|-----------|-----|----------|----------|
| low | 0.820 | 0.126 | 0.813 | 0.820 | 0.816 | 0.693 | 0.891 | 0.823 |
| mid | 0.782 | 0.118 | 0.767 | 0.782 | 0.775 | 0.661 | 0.884 | 0.750 |
| high | 0.890 | 0.027 | 0.924 | 0.890 | 0.907 | 0.874 | 0.945 | 0.905 |
| **Weighted Avg.** | 0.826 | 0.096 | 0.828 | 0.826 | 0.827 | 0.731 | 0.903 | 0.821 |

**[CAPTURA 11 — Curva ROC y área bajo la curva (una clase frente al resto).]**

**[CAPTURA 12 — Comparación gráfica del `%error` entre los 4 algoritmos.]**

### 8.5 Ejemplo de predicciones individuales

Las tres primeras instancias del conjunto de validación, con su vecino más cercano en el
entrenamiento. Se generaron con la misma configuración de la corrida de 8.2 (`IBk`, k=1, distancia
euclidiana), de modo que las predicciones coinciden con las reportadas por Weka.

| # | Age | SystolicBP | DiastolicBP | BS | BodyTemp | HeartRate | Real | Vecino 1-NN (train) | Distancia | Predicha | ¿Acierto? |
|---|-----|-----------|-------------|-----|----------|-----------|------|-----------------------|-----------|----------|-----------|
| 1 | 35 | 140 | 90 | 13.0 | 98.0 | 70 | high | DiastolicBP=80, resto idéntico → **high** | 0.1961 | high (p=0.997) | Sí |
| 2 | 30 | 140 | 85 | 7.0 | 98.0 | 70 | high | **Idéntica** → high | 0.0000 | high (p=0.997) | Sí |
| 3 | 23 | 130 | 70 | 7.01 | 98.0 | 78 | mid | BS=6.8, resto idéntico → mid | 0.0162 | mid (p=0.999) | Sí |

Las tres predicciones son correctas, y la segunda ilustra el caso limite de `IBk`: la instancia de
test es **exactamente** una fila del entrenamiento (distancia 0.0000), así que el modelo la
reconoce de memoria. Este comportamiento se repite a gran escala: **219 de las 305 instancias de
validación (71.8 %) tienen un patrón de valores que ya existe en el conjunto de entrenamiento**. Es
una limitación de la partición aleatoria sobre un dataset con 562 filas duplicadas exactas, y
significa que los accuracies de la tabla 8.2 están inflados respecto de lo que ocurriría con
pacientes nuevas reales. Este matiz se desarrolla en la sección de limitaciones.

---

## 9. Análisis y discusión de resultados

<!-- Completar una vez que se tengan los números de la sección 9 -->

### 9.1 Criterios de comparación

Para elegir el clasificador final se consideraron cuatro criterios, en este orden de prioridad
clínica:

1. **Kappa statistic (`1kappa`):** es la métrica principal, porque a diferencia del accuracy
   (exactitud) corrige el desempeño por azar. En problemas de salud con clases cercanas entre
   sí, un accuracy alto puede ser engañoso; un **kappa cercano a 1** indica un modelo que
   realmente discrimina `low`, `mid` y `high risk`.
2. **%error en el conjunto de prueba (generalización):** la capacidad de funcionar con pacientes
   nuevos es el requisito real de un modelo que se aplique en consulta.
3. **Exhaustividad (recall) de la clase `high risk`:** desde el punto de vista de salud pública,
   **es preferible clasificar de más a una paciente de riesgo alto que dejar pasar un caso
   grave**. Un falso negativo en salud materna tiene un costo mucho mayor que un falso positivo.
4. **Tiempo de entrenamiento y complejidad del modelo:** un modelo que tarde 0.02 s es
   utilizable en la práctica; uno que tarde minutos, no.

### 9.2 Interpretación de la brecha train / test

La diferencia entre la tabla de entrenamiento (sección 9.1) y la de validación (sección 9.2)
es el indicador de **sobreajuste**:

- **Brecha pequeña (< 5 %):** el modelo generaliza bien. Es el escenario deseado.
- **Brecha grande (> 10 %):** el modelo memorizó el entrenamiento. Causas probables: demasiadas
  unidades neuronas con pocas muestras, o un K muy bajo en IBk.
- En este dataset, es esperable que **IBk y SVM** muestren métricas de entrenamiento
  prácticamente perfectas (100 % de aciertos) por la alta repetición de registros descrita en
  6.4, y que su desempeño en prueba se reduzca. Esa brecha debe reportarse explícitamente.

![[Pasted image 20260926181407.png]]

### 9.3 Limitaciones del estudio

- **Tamaño de muestra reducido** (1,014 registros) y proviene de un solo país (Bangladesh);
  los hallazgos no se generalizan a otras poblaciones sin reentrenamiento.
- **Duplicados en el dataset** (166 registros aparecen en train y test) inflan de forma
  optimista las métricas de los clasificadores por distancia.
- **Valores atípicos** de `HeartRate` no corregidos (2 registros con 7 bpm).
- **Multiclase con clases cercanas:** `low risk` y `mid risk` pueden no ser separables de forma
  nítida con solo estas 6 variables. Un desempeño cercano al azar en esas dos clases es un
  resultado **esperable y científicamente honesto**, no un error del experimento.
- **Sin validación clínica:** las etiquetas `RiskLevel` provienen del criterio clínico de las
  mediciones registradas, no de un estudio clínico prospectivo.

### 9.4 Trabajo futuro

1. Reentrenar con la eliminación de duplicados para medir el impacto real del solapamiento.
2. Añadir más variables clínicas (hemoglobina, peso, altura, antecedentes obstétricos) para
   intentar separar mejor `low risk` de `mid risk`.
3. Probar modelos más potentes y métodos de conjunto (por ejemplo, Random Forest o XGBoost),
   que en trabajos previos con este mismo dataset superaron a los clasificadores
   individuales aquí evaluados.
4. Sustituir la predicción dura por una **salida probabilística** (probabilidades por clase),
   lo que permitiría un umbral de alarma configurable según la sensibilidad requerida
   por el protocolo clínico.

---

## 10. Conclusiones

1. El dataset **Maternal Health Risk** de la UCI es adecuado para un ejercicio de
   clasificación multiclase porque combina tamaño manejable, atributos numéricos de bajo costo,
   cero valores faltantes y un objetivo con impacto directo en la salud pública.

2. La preparación de los datos fue un paso crítico: se particionó el dataset en
   **70 % entrenamiento (709 registros) y 30 % prueba (305 registros)** de manera
   **estratificada**, verificando que la distribución de clases se conservara con una desviación
   máxima de **0.06 p.p.**, y se confirmando que las medias y rangos de cada variable fueran
   equivalentes en ambos subconjuntos.

3. La comparación de los cuatro clasificadores bajo un **protocolo idéntico** (mismos datos,
   misma semilla, mismas métricas) permite atribuir las diferencias de desempeño
   exclusivamente al algoritmo, que es lo que se busca en un experimento comparativo.

4. El uso de **Kappa statistic** como métrica principal evita caer en la trampa del accuracy
   (exactitud) en un problema de salud con clases cercanas, y la matriz de confusión permite
   identificar exactamente qué confusiones son clínicamente relevantes.

5. Más allá de los números, el proyecto demuestra que **seis constantes vitales de bajo costo
   pueden alimentar un sistema de alerta temprana de riesgo materno** aplicable en contextos
   rurales con escasez de personal especializado — una contribución al Objetivo de Desarrollo
   Sostenible 3 de las Naciones Unidas.

---

## 11. Referencias

1. **Ahmed, M. (2020).** *Maternal Health Risk* [Conjunto de datos, ID 863]. UCI Machine
   Learning Repository, Irvine (California, EE. UU.). Fecha de donación: 14 de agosto de 2023.
   <https://archive.ics.uci.edu/dataset/863/maternal+health+risk>
   DOI: <https://doi.org/10.24432/C5DP5D>
   **Fuente primaria de los datos** empleados en este proyecto. Licencia CC BY 4.0: la
   réutilización exige citar a la autora y al repositorio, atribución que se hace en las
   secciones 4.1 y 6.2 de este documento.

2. **Ahmed, M., Kashem, M. A., Rahman, M., & Khatun, S. (2020).** Review and Analysis of Risk
   Factor of Maternal Health in Remote Area Using the Internet of Things (IoT). En
   *Lecture Notes in Electrical Engineering*, vol. 632, pp. 357–365 (InECCE2019).
   Springer Singapore. <https://doi.org/10.1007/978-981-15-2317-5_30>
   Artículo que acompaña al dataset: describe el proceso de recolección de los datos y
   justifica las seis variables como factores de riesgo de mortalidad materna (sección 5.6).

3. **Togunwa, T. O., Babatunde, A. O., & Abdullah, K.-u.-R. (2023).** Deep hybrid model for
   maternal health risk classification in pregnancy: synergy of ANN and random forest.
   *Frontiers in Artificial Intelligence*, 6, 1213436.
   <https://doi.org/10.3389/frai.2023.1213436>
   Antecedente directo: usa este mismo dataset y reporta el desempeño de KNN, SVM y Naive Bayes
   frente a un modelo híbrido (sección 5.1).

4. **Venkatesh, S., Jha, H., Kazmi, F., & Zaidi, S. (2024).** Classification of Maternal Health
   Risks Using Machine Learning Methods. En *Advances in Digital Health and Medical
   Bioengineering (EHB 2023)*, IFMBE Proceedings, vol. 109. Springer, Cham.
   <https://doi.org/10.1007/978-3-031-62502-2_91>
   Antecedente directo: compara KNN, SVM y otros clasificadores sobre este dataset
   (sección 5.1).

5. **Organización Mundial de la Salud.** *Maternal mortality* (Factsheet, 7 de abril de 2025).
   <https://www.who.int/news-room/fact-sheets/detail/maternal-mortality>
   Define las causas de muerte materna y su carácter prevenible (secciones 2.1 y 5.7).

6. **Naciones Unidas.** *Objetivo de Desarrollo Sostenible 3: Salud y Bienestar*.
   <https://sdgs.un.org/goals/goal3>
   Meta 3.1: reducir la mortalidad materna a menos de 70 muertes por cada 100,000/SCS,
   marco en el que se justifica la relevancia del problema (secciones 1, 3 y 11).

7. **Witten, I. H., Frank, E., Hall, M. A., & Pal, C. J. (2016).** *Data Mining: Practical
   Machine Learning Tools and Techniques* (4.ª ed.). Morgan Kaufmann.
   Base teórica de los cuatro algoritmos del marco teórico (secciones 5.2 a 5.5), de los
   conceptos de validación train/test y de las métricas de desempeño, incluido el
   *Kappa statistic* analizado en la sección 10.

> El particionado de los datos (sección 6.2) se realizó con `scikit-learn`, una biblioteca
> abierta de uso común en aprendizaje automático; no se cita de forma específica porque
> interviene únicamente como herramienta auxiliar de preparación de datos, no como fuente
> de conocimiento propio del trabajo.
