# Sistema Experto para la Decisión del Tipo de Cesárea — Interfaz Web

> Práctica: sistema experto con **encadenamiento hacia atrás** en Prolog, ahora expuesto a través de una **interfaz web** (servidor HTTP + HTML generado por el propio Prolog, sin JavaScript). El motor de inferencia es el mismo de `cesareas.pl`; esta versión (`cesareas_web.pl`) sustituye la consola por un formulario y una página de resultados con iconografía.

## 1. Objetivo de la práctica

Construir un **sistema experto** capaz de decidir el **tipo de cesárea** (prevista de antemano o improvisada durante el parto) y la **incisión abdominal** a realizar, a partir de una serie de características clínicas del caso. La práctica añade a la versión de consola una **interfaz de usuario web** que:

- presenta las características clínicas como **casillas de verificación** ilustradas con iconos;
- recoge la entrada del usuario mediante un `POST` de formulario;
- ejecuta el motor de inferencia y muestra el **diagnóstico**, la **incisión**, la información de la incisión y las **fases de la intervención**.

Toda la interfaz se genera **desde Prolog** con `library(http/html_write)` (DCGs), de modo que no se escribe HTML a mano ni se usa JavaScript.

## 2. Arquitectura de la interfaz web

### 2.1 Tecnologías

| Componente | Módulo/librería |
|:---|:---|
| Servidor HTTP | `library(http/thread_httpd)` |
| Enrutado por rutas | `library(http/http_dispatch)` |
| Generación de HTML | `library(http/html_write)` |
| Servido de ficheros estáticos (SVG) | `library(http/http_files)` |
| Lectura del cuerpo del `POST` | `library(http/http_client)` |
| Motor de inferencia | predicados `hipotesis/2`, `cesarea_prevista_de_antemano/0`, `cesarea_improvisada_durante_el_parto/0` |

### 2.2 Rutas y handlers

El servidor se levanta con `http_dispatch` (no con un único goal) para que **cada ruta** tenga su handler:

```prolog
:- http_handler('/', inicio, []).
:- http_handler('/diagnosticar', diagnosticar, []).
:- http_handler('/imgs', http_reply_from_files('web/imgs', []), [prefix]).

servidor :-
      http_server(http_dispatch, [port(3939)]),
      format('Servidor web activo en http://localhost:3939/~n'),
      thread_get_message(_).
```

| Ruta | Método | Handler | Función |
|:---|:---:|:---|:---|
| `/` | GET | `inicio/1` | Formulario con las 12 características (dos campos: prevista / improvisada) |
| `/diagnosticar` | POST | `diagnosticar/1` | Ejecuta la inferencia y muestra el resultado |
| `/imgs/<archivo>.svg` | GET | `http_reply_from_files/2` | Sirve los iconos como `image/svg+xml` |

### 2.3 Entrada de datos: conversión a hechos `y/1` y `n/1`

El formulario envía `name=si` por cada casilla marcada. El handler lee el cuerpo con `http_read_data/3`, que parsea automáticamente `application/x-www-form-urlencoded` a una lista de términos `Nombre=Valor`:

```prolog
diagnosticar(Request) :-
      memberchk(method(post), Request),
      http_read_data(Request, FormData, []),   % parsea el formulario
      cargar_hechos(FormData),                 % assertz y/1  ó  n/1
      hipotesis(Cesarea, Incision),
      with_output_to(string(Informacion), detalle_incision(Incision)),
      with_output_to(string(Fases), detalle_fases),
      reply_html_page(
          [title('Diagnóstico - Sistema Experto Cesáreas')],
          \pagina_diagnostico(Cesarea, Incision, Informacion, Fases)),
      limpiar_hechos.                          % deja limpia la base para el siguiente caso
```

```prolog
cargar_hechos(FormData) :-
      retractall(y(_)),
      retractall(n(_)),
      caracteristicas(Lista),
      maplist(cargar_hecho(FormData), Lista).

cargar_hecho(FormData, F) :-
      ( is_list(FormData),
        memberchk(F='si', FormData)
      -> assertz(y(F))
      ;  assertz(n(F))
      ).
```

Cada característica no marcada se registra como `n/1`, de modo que `verify/1` (que consulta `y/1` y `n/1`) obtiene siempre una respuesta. En la web **nunca se pregunta por consola**: `ask_web/1` falla y toda la información proviene del formulario.

### 2.4 Estilo visual

La hoja de estilo va embebida en la página (`css_base/1`) y usa una paleta neutra (Tailwind *neutral*) con acentos semánticos (rojo para sangre/placenta, verde para positivo, amarillo para alerta):

```prolog
body{font-family:Segoe UI,system-ui,Arial,sans-serif;max-width:880px;margin:48px auto;
     color:#262626;background:#fafafa}
h1{color:#171717;font-size:26px;font-weight:700;border-bottom:2px solid #171717}
fieldset{border:1px solid #e5e5e5;border-radius:10px;padding:16px 20px;background:#fff}
label img.ico{width:48px;height:32px;object-fit:contain;border:1px solid #e5e5e5;border-radius:6px}
button{background:#171717;color:#fff;border:none;border-radius:8px}
```

Los **iconos** son ficheros SVG servidos por `/imgs` (estilo *flat*, `viewBox 0 0 200 130`), uno por característica, más los de resultado/incisión y el diagrama de fases.

## 3. Red semántica del dominio

Se conserva la red semántica de la práctica original: **hechos** (características que el sistema verifica) y **reglas** R1–R10 (implicaciones `si … entonces …`). Una flecha se lee «implica»; cuando varias causas comparten flecha basta con que **alguna** se confirme.

![[Pasted image 20260917180916.png]]

| Regla | Condición | Conclusión |
|:---:|:---|:---|
| R1 | posición podálica | cesárea prevista de antemano |
| R2 | gestosis **o** diabetes gravídica | cesárea prevista de antemano |
| R3 | placenta previa-central | cesárea prevista de antemano |
| R4 | problemas de corazón **o** renales **o** infecciones | cesárea prevista de antemano |
| R5 | cabeza demasiado grande | cesárea improvisada |
| R6 | cabeza no encajada | cesárea improvisada |
| R7 | ritmo cardíaco irregular **y** meconio | sufrimiento fetal |
| R8 | placenta desprendida | cesárea improvisada |
| R9 | improvisada **y** placenta desprendida | incisión umbílico-púbica |
| R10 | prevista, o improvisada sin placenta desprendida | incisión transversal baja o de Joel Coell |

## 4. Características e iconografía

En la interfaz cada característica clínica muestra su icono junto a la etiqueta:

| # | Característica | Icono |
|:---:|:---|:---|
| 1 | Bebé en posición podálica | `podalica.svg` |
| 2 | Gestosis (hipertensión del embarazo) | `gestosis.svg` |
| 3 | Diabetes gravídica | `diabetes.svg` |
| 4 | Placenta previa-central | `placenta_previa.svg` |
| 5 | Problemas de corazón de la madre | `corazon.svg` |
| 6 | Problemas renales de la madre | `renales.svg` |
| 7 | Infecciones en vías genitales | `infecciones.svg` |
| 8 | Cabeza demasiado grande | `cabeza_grande.svg` |
| 9 | Cabeza no encajada | `cabeza_no_encajada.svg` |
| 10 | Ritmo cardíaco fetal irregular | `ritmo_irregular.svg` |
| 11 | El bebé expulsa meconio | `meconio.svg` |
| 12 | La placenta se desprende | `placenta_desprendida.svg` |

Resultados e incisión: `resultado_prevista.svg`, `resultado_improvisada.svg`, `incision_vertical.svg`, `incision_transversal.svg`, `sin_diagnostico.svg` y el diagrama de las 4 fases `fases.svg`.

## 5. Pruebas ejecutadas en la interfaz

Se replican los **cuatro casos** del documento original, ahora marcando las casillas en la interfaz web.

### 5.1 Formulario inicial

Al abrir `http://localhost:3939/` se muestran las dos etapas con sus casillas e iconos:

![[capturas/ui_1_formulario.png]]

### 5.2 Corrida 1 — Cesárea prevista (posición podálica)

Se marca **«El bebé está en posición podálica»** y se pulsa *Diagnosticar*:

![[capturas/ui_2_prevista_podalica.png]]

### 5.3 Corrida 2 — Cesárea prevista (diabetes gravídica)

Se marca **«La madre padece diabetes gravídica»**:

![[capturas/ui_3_prevista_diabetes.png]]

### 5.4 Corrida 3 — Cesárea improvisada con incisión umbílico-púbica

Se marcan **«La cabeza del bebé es demasiado grande»** y **«La placenta se desprende»**:

![[capturas/ui_4_improvisada_umbilicopubica.png]]

### 5.5 Corrida 4 — Cesárea improvisada con incisión transversal

Se marcan **«El ritmo cardíaco del bebé es irregular»** y **«El bebé expulsa meconio»** (sufrimiento fetal):

![[capturas/ui_5_improvisada_transversal.png]]

### 5.6 Resumen de los casos probados

| Corrida | Casillas marcadas | Diagnóstico (cesárea) | Incisión |
|:---:|:---|:---|:---|
| 1 | posición podálica | prevista de antemano | transversal baja o Joel Coell |
| 2 | diabetes gravídica | prevista de antemano | transversal baja o Joel Coell |
| 3 | cabeza grande + placenta desprendida | improvisada durante el parto | umbílico-púbica |
| 4 | ritmo irregular + meconio | improvisada durante el parto | transversal baja o Joel Coell |

Casos adicionales verificados: un formulario **sin ninguna casilla** devuelve «sin diagnóstico / sin decidir» (con el icono neutro `sin_diagnostico.svg`), y cada una de las siete características de la primera etapa conduce por sí sola a «cesárea prevista de antemano».

## 6. Cómo ejecutar

```bash
# 1. Situarse en el directorio del proyecto (donde está web/imgs)
cd prolog-workspace

# 2. Arrancar el servidor
swipl -s cesareas_web.pl -g servidor

# 3. Abrir en el navegador
#    http://localhost:3939/
```

El servidor se queda a la escucha en el puerto **3939**. Para detenerlo, `Ctrl+C` o cerrar el proceso.

## 7. Referencias

1. World Health Organization (WHO). *WHO statement on caesarean section rates*. Ginebra: WHO; 2015. WHO/RHR/15.02. Disponible en: https://www.who.int/publications/i/item/WHO-RHR-15.02
2. Hofmeyr GJ, Mathai M, Shah A, Novikova N. *Techniques for caesarean section*. Cochrane Database Syst Rev. 2008;(1):CD004662. DOI: 10.1002/14651858.CD004662.pub2
3. National Institute for Health and Care Excellence (NICE). *Caesarean birth*. NICE guideline NG192. Londres: NICE; 2021 (actualizado). Disponible en: https://www.nice.org.uk/guidance/ng192
4. Gray C, Shanahan M. *Breech Presentation*. StatPearls [Internet]. Treasure Island (FL): StatPearls Publishing; 2026. Bookshelf ID: NBK448063. Disponible en: https://www.ncbi.nlm.nih.gov/books/NBK448063/
5. Oyelese Y, Smulian JC. *Placenta previa, placenta accreta, and vasa previa*. Obstet Gynecol. 2006;107(4):927-941.
6. Mylonas I, Friese K. *Indications for and Risks of Elective Cesarean Section*. Dtsch Arztebl Int. 2015;112(29-30):489-495.
7. Mathai M, Hofmeyr GJ, Mathai NE. *Abdominal surgical incisions for caesarean section*. Cochrane Database Syst Rev. 2021;(8):CD004453. DOI: 10.1002/14651858.CD004453.pub3
