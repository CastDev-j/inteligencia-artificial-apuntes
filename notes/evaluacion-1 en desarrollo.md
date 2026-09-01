# Examen - Sistemas Expertos y Lógica

---

## Parte 1: Emparejamiento de conceptos (40 pts)

| # | Concepto | Definición |
|---|---|---|
| 1713 | **Prueba de Turing** | Un humano interroga a un ordenador por teléfono; si no distingue si es humano o máquina, se supera la prueba |
| 1106 | **Aristóteles** | Primero en codificar silogismos |
| 1046 | **PLN** | Procesamiento de Lenguaje Natural — subcampo de la computación y el lenguaje humano |
| 1555 | **Sintáctico** | A partir de unidades léxicas se genera estructura representativa (árbol o red) |
| 1485 | **Conocimientos para ML** | Lingüística, Ciencia de la Computación, Estadística Bayesiana, Álgebra Lineal, Teoría de la Optimización |
| 1380 | **Reconocimiento de patrones** | Ciencia que ocupa procesos de ingeniería, computación y matemáticas con objetos físicos o abstractos |
| 1597 | **Espacio de estados** | Representación de un problema que abarca todas las situaciones posibles en la solución |
| 1740 | **Estrategias de búsqueda** | Guiada por datos (forward), guiada por objetivos (backward), búsqueda ciega, primero en profundidad, primero en anchura |
| 1512 | **Análisis sintáctico** | Utiliza estructura semántica para interpretación final de la oración según contexto |
| 1704 | **Emulación** | Actuar como en la realidad sin importar los procesos internos |
| 1792 | **Espacios de estados** | Definición formal |
| 1520 | **Búsqueda heurística** | Difícil establecer el objetivo desde el principio |
| 1464 | **Búsqueda exhaustiva** | Backtracking / fuerza bruta |
| 1698 | **Aprender** | Adquirir conocimiento por estudio o experiencia |
| 1848 | **Zadeh** | Introdujo el concepto de subconjunto borroso / lógica difusa |
| 1619 | **Agente inteligente** | Entidad capaz de percibir y actuar, resuelve problemas con soluciones parciales a menudo intuidas |
| 1842 | **Inteligencia Artificial** | Estudio de cómo lograr que computadoras hagan tareas que los humanos hacen mejor |
| 1737 | **Robot / Agente autónomo** | Máquina programable capaz de percibir y actuar con autonomía |
| 1648 | **Lógica difusa** | Conjuntos borrosos |
| 1712 | *Sin identificar* | Posiblemente error tipográfico o nombre propio sin relevancia |

---

## Parte 2: Respuestas completas

### 1. Predicados monádicos y poliádicos

**Monádicos** (aridad 1):

```prolog
es_mujer(ana).
es_hombre(juan).
es_estudiante(carlos).
```

**Poliádicos** (aridad 2 o más):

```prolog
padre(juan, ana).          % aridad 2
gusta(maria, chocolate).   % aridad 2
envia(juan, carta, ana).   % aridad 3
```

---

### 2. Variables anónimas

> Al escribir un predicado, una variable anónima puede aparecer varias veces

**Falso.** Cada `_` es independiente. Si se necesita que sea la misma variable, se debe usar un nombre concreto (ej. `X`).

---

### 3. Representación en Prolog de ∀x

```prolog
es_divisible_por_dos(X) :- par(X).
```

> **Nota:** La aridad de `es_divisible_por_dos/1` es 1. El cuantificador universal `∀` se omite en Prolog porque todas las variables en la cabeza de una regla se consideran universalmente cuantificadas.

---

### 4. Operadores dinámicos en Prolog

Son aquellos declarados con `:- dynamic predicado/aridad`. Permiten modificar la base de conocimientos en tiempo de ejecucción con `assert/1`, `retract/1` y `abolish/1`.

```prolog
:- dynamic mi_hecho/2.
```

---

### 5. ¿Para qué sirve el evaluador?

El evaluador (motor de inferencia) sirve para sintetizar un valor o determinar si una consulta es verdadera, mediante:

- **Unificación**
- **Backtracking**
- **Aplicación de reglas y hechos**

En Prolog, es el núcleo que resuelve objetivos.

---

### 6. Otra definición de predicado

También se define como **relación** o **estructura relacional**, porque establece una relación entre sus argumentos (no es una función que devuelve un valor).

---

### 7. ¿Por qué no se declaran las variables en Prolog?

Porque las variables se instancian automáticamente mediante **unificación** durante la ejecución. No hay tipos declarados; una variable puede tomar cualquier valor que encaje con la consulta.

---

### 8. Paradigmas de la programación lógica

- **Declarativo** — se describe qué se quiere, no cómo
- **Basado en reglas** — hechos + reglas de inferencia
- **Lógico-matemático** — basado en lógica de predicados de primer orden

---

### 9. Estructura de una cláusula

Una cláusula está compuesta por **cabeza** (conclusión) y **cuerpo** (premisas), separados por `:-`.

| Tipo | Estructura | Ejemplo |
|---|---|---|
| **Hecho** | Solo cabeza | `padre(juan, ana).` |
| **Regla** | `cabeza :- cuerpo` | `abuelo(X,Z) :- padre(X,Y), padre(Y,Z).` |

---

### 10. Representación en Prolog de una expresión

Dada: `mujer(hormiga) → hombre(mutín), hombre(frigo) → pareja(hormiga,mutín), conductor, padre(Javier, ericita)`

```prolog
mujer(hormiga).
hombre(mutín).
hombre(frigo).
pareja(hormiga, mutín).
conductor.
padre(javier, ericita).

t :- mujer(hormiga), hombre(mutín), hombre(frigo),
      pareja(hormiga, mutín), conductor, padre(javier, ericita).
```

> La flecha `→` se interpreta como implicación (`:-` en Prolog`). `t` sería la meta que se cumple si todos los hechos y reglas son verdaderos.
