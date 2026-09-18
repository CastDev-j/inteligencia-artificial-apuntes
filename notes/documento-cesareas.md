# Sistema Experto para la Decisión del Tipo de Cesárea

## 1. Investigación

### 1.1 Definición y contexto

La cesárea es un procedimiento quirúrgico que consiste en extraer al feto, la placenta y las membranas a través de incisiones en la pared abdominal y en el útero [2]. Desde 1985 la comunidad internacional de salud consideró que la tasa ideal de cesáreas debía situarse entre el 10 % y el 15 % de los partos [1]. Sin embargo, análisis posteriores de la OMS mostraron que cuando la tasa de cesáreas supera el ~10 % a nivel poblacional no se observan reducciones adicionales en la mortalidad materna o neonatal, por lo que hoy se enfatiza en «no perseguir una tasa específica sino ofrecer cesáreas a toda mujer que las necesite» [1]. Para comparar tasas entre instituciones, la OMS recomienda la **clasificación de Robson** (10 grupos) como estándar internacional [1].

### 1.2 Cesárea programada (prevista) vs. improvisada (de urgencia)

Desde el punto de vista clínico, la cesárea se clasifica según la **urgencia** de la decisión [3]:

- **Cesárea programada / prevista de antemano:** se decide antes del inicio del trabajo de parto. Algunas indicaciones clásicas son la presentación podálica a término (ofreciendo antes una versión cefálica externa) [3][4], la **placenta previa** (indicación absoluta de cesárea) [5], y enfermedades maternas asociadas al embarazo como síndromes hipertensivos (gestosis) o diabetes [6].
- **Cesárea improvisada / de urgencia:** se decide durante el trabajo de parto. Entre sus causas típicas se encuentran la desproporción cefalopélvica (cabeza fetal demasiado grande para el canal del parto), la mala encajamiento de la presentación, el **sufrimiento fetal** (alteración del ritmo cardíaco fetal, asociada a menudo a líquido amniótico meconial) y el desprendimiento de placenta [2][3]. En los casos de compromiso fetal agudo se recomienda realizar la extracción lo antes posible (estándar aceptado: < 30 minutos) [3].

### 1.3 Tipos de incisión abdominal

Las incisiones abdominales para cesárea se dividen en **verticales** (mediana baja) y **transversales** [7]:

- **Incisión vertical (p. ej., Umbílico-pública):** se extiende desde la región umbilical hasta el pubis; produce una cicatriz visible y grande. Se asocia a mayor morbilidad de herida que las transversales, por lo que hoy se reserva para situaciones de urgencia extrema o casos específicos [2][7].
- **Incisión transversal baja (Pfannenstiel):** incisión curvilínea transversa ligeramente por encima del pubis; es la incisión ginecológica más utilizada en la actualidad y se asocia a menor dolor y mejores resultados estéticos (cicatriz poco visible) [7].
- **Incisión de Joel-Cohen (base del método Misgav-Ladach):** incisión transversal recta, algo más alta y superficial que Pfannenstiel, con disección roma de los planos. Una revisión Cochrane y varios metaanálisis muestran que las técnicas basadas en Joel-Cohen reducen el **tiempo quirúrgico, la pérdida de sangre y la estadía hospitalaria** respecto de Pfannenstiel [2][7].

### 1.4 Fases de la intervención

Con independencia del tipo de incisión, la cesárea transcurre siempre en el mismo orden de tiempos quirúrgicos: (1) apertura abdominal y del útero, (2) extracción del bebé, (3) extracción de la placenta y membranas, y (4) sutura de la herida [2].

---

## 2. Red semántica del dominio

La red semántica se reduce a los **hechos** (características del caso que el sistema pregunta) y las **reglas** R1–R10 del documento. Una flecha `→` se lee «implica» (regla del experto); la unión de varias causas en una misma flecha indica que basta con que **alguna** (o las **y** cuando se indica) se confirme:

![[Pasted image 20260917180916.png]]

> **Leyenda:**
> - Los **hechos** son los antecedentes que el sistema verifica preguntando (`verify/1` + `ask/1`).
> - Las **reglas** R1–R10 son las implicaciones `si ... entonces ...` modeladas:
>   - **R1–R4:** posición podálica, gestosis/diabetes gravídica, placenta previa-central o problemas de la madre → **cesárea prevista de antemano** (cualquiera de ellas alcanza).
>   - **R7:** sufrimiento fetal = ritmo cardíaco irregular **y** expulsión de meconio.
>   - **R5–R8:** cabeza demasiado grande, cabeza no encajada, sufrimiento fetal o desprendimiento de placenta → **cesárea improvisada**.
>   - **R9:** cesárea no programada **y** placenta desprendida → incisión **umbílico-púbica**.
>   - **R10:** en el resto de los casos → incisión **transversal baja o Joel Coell**.

---

## 3. Modelado en Prolog

El sistema experto sigue la arquitectura base de `animals.pl`:

- Encadenamiento hacia atrás (`hipotesis/2` → predicados `cesarea_prevista_de_antemano/0` y `cesarea_improvisada_durante_el_parto/0`).
- Verificación de hechos con encuesta al usuario (`verify/1` + `ask/1`) y memoria de los hechos `y/1` y `n/1` (assert/retract).
- Base de reglas declarativa con operadores `si · entonces · y · o · no`.
- Principio de **regla disparada por la primera causa confirmada** (cortes `!`): el diagnóstico `prevista`, `improvisada` y la incisión se emiten por orden.

Estructura de la decisión:

![[Pasted image 20260917181006.png]]

---

## 4. Código de ejecución

### 4.1 Código fuente (`cesareas.pl`)

```prolog
/***************************PLF****************/
/******************SISTEMA EXPERTO CESÁREAS***********************/

:- encoding(utf8).

:- dynamic y/1.
:- dynamic n/1.

% DECLARACIÓN DE LOS OPERADORES

:- op(1115, fx, si).
:- op(1110, xfy, entonces).
:- op(1100, xfy, o).
:- op(1000, xfy, y).
:- op(900, fx, no).


% CONOCIMIENTO DEL EXPERTO (reglas declarativas)

% --- Cesárea prevista de antemano ---
% R1: posición podálica del bebé
regla(si bebe_esta_en_posicion_podalica(Embarazo) entonces cesarea_prevista_de_antemano(Embarazo)).

% R2: enfermedad durante el embarazo (gestosis o diabetes gravídica)
regla(si la_madre_padece_gestosis(Embarazo) o la_madre_padece_diabetes_gravida(Embarazo) entonces cesarea_prevista_de_antemano(Embarazo)).

% R3: placenta previa-central
regla(si placenta_esta_en_posicion_previa_central(Embarazo) entonces cesarea_prevista_de_antemano(Embarazo)).

% R4: problemas de la madre (corazón, renales o infecciones en vías genitales)
regla(si la_madre_tiene_problemas_de_corazon(Madre) o la_madre_tiene_problemas_renales(Madre) o la_madre_tiene_infecciones_en_vias_genitales(Madre) entonces cesarea_prevista_de_antemano(Madre)).

% --- Cesárea improvisada durante el parto ---
% R5: cabeza demasiado grande
regla(si cabeza_del_bebe_es_demasiado_grande(Parto) entonces cesarea_improvisada_durante_el_parto(Parto)).
% R6: cabeza no encajada
regla(si cabeza_del_bebe_no_esta_encajada(Parto) entonces cesarea_improvisada_durante_el_parto(Parto)).
% R7: sufrimiento fetal (ritmo cardíaco irregular y expulsa meconio)
regla(si ritmo_cardiaco_del_bebe_es_irregular(Parto) y bebe_expulsa_meconio(Parto) entonces sufrimiento_fetal(Parto)).
regla(si sufrimiento_fetal(Parto) entonces cesarea_improvisada_durante_el_parto(Parto)).
% R8: la placenta se desprende
regla(si la_placenta_se_desprende(Parto) entonces cesarea_improvisada_durante_el_parto(Parto)).

% --- Tipo de incisión ---
% R9: cesárea no programada + placenta desprendida -> umbílico-púbica
regla(si cesarea_improvisada_durante_el_parto(Parto) y la_placenta_se_desprende(Parto) entonces incision_umbilicopubica(Parto)).
% R10: resto de los casos -> transversal baja o de Joel Coell
regla(si cesarea_prevista_de_antemano(Embarazo) entonces incision_transversal_baja_o_joel_coell(Embarazo)).
regla(si cesarea_improvisada_durante_el_parto(Parto) o no la_placenta_se_desprende(Parto) entonces incision_transversal_baja_o_joel_coell(Parto)).


% EJECUTAR EL PROGRAMA
identificar :- hipotesis(Cesarea, Incision),
      nl,
      write('Pienso que la cesárea es de tipo : '),
      write(Cesarea),
      nl,
      write('La incisión a realizar es : '),
      write(Incision),
      nl,
      nl,
      write('Información sobre el tipo de incisión : '),
      nl,
      mostrar_incision(Incision),
      nl,
      write('Fases de la intervención (siempre en este orden) : '),
      nl,
      fases_de_la_intervencion,
      undo.


% HIPOTESIS
hipotesis("cesárea prevista de antemano", "transversal baja o de Joel Coell")
     :- cesarea_prevista_de_antemano, !.

hipotesis("cesárea improvisada durante el parto", "umbílico-púbica")
     :- cesarea_improvisada_durante_el_parto,
        verify(la_placenta_se_desprende), !.

hipotesis("cesárea improvisada durante el parto", "transversal baja o de Joel Coell")
     :- cesarea_improvisada_durante_el_parto, !.

hipotesis("sin diagnóstico", "sin decidir").    /* sin diagnóstico */


% VERIFICAR REGLAS

% Cesárea prevista de antemano: si se da alguna de estas circunstancias
cesarea_prevista_de_antemano :-
      ( verify(bebe_esta_en_posicion_podalica)
      ; verify(la_madre_padece_gestosis)
      ; verify(la_madre_padece_diabetes_gravida)
      ; verify(placenta_esta_en_posicion_previa_central)
      ; verify(la_madre_tiene_problemas_de_corazon)
      ; verify(la_madre_tiene_problemas_renales)
      ; verify(la_madre_tiene_infecciones_en_vias_genitales)
      ), !.

% Cesárea improvisada: si se da alguna de estas circunstancias
cesarea_improvisada_durante_el_parto :-
      ( verify(cabeza_del_bebe_es_demasiado_grande)
      ; verify(cabeza_del_bebe_no_esta_encajada)
      ; sufrimiento_fetal
      ; verify(la_placenta_se_desprende)
      ), !.

% Sufrimiento fetal: ritmo cardíaco irregular y expulsa meconio
sufrimiento_fetal :-
      verify(ritmo_cardiaco_del_bebe_es_irregular),
      verify(bebe_expulsa_meconio).


% INFORMACIÓN SOBRE CADA TIPO DE INCISIÓN
mostrar_incision("umbílico-púbica") :-
      write('  - Es vertical, empieza debajo del ombligo y termina en el pubis.'), nl,
      write('  - La cicatriz es visible y grande.'), nl.

mostrar_incision("transversal baja o de Joel Coell") :-
      write('  - Transversal baja : es horizontal, la cicatriz no es visible.'), nl,
      write('  - De Joel Coell : es horizontal.'), nl.

mostrar_incision(_) :-
      write('  - No hay suficiente información.'), nl.


% FASES DE LA INTERVENCIÓN (siempre iguales y en este orden)
fases_de_la_intervencion :-
      write('  1) Cortar.'), nl,
      write('  2) Extraer al niño.'), nl,
      write('  3) Extraer la placenta.'), nl,
      write('  4) Suturar la herida.'), nl.


% SALIDA AL EDITOR
ask(Question) :-
    write('El caso presenta la siguiente característica : '),
    write(Question),
    write('? '),
    read(Response),
    nl,
    ( (Response == yes ; Response == y)
      ->
       assert(y(Question)) ;
       assert(n(Question)), fail).

verify(S) :-
   (y(S)
    ->
    true ;
    (n(S)
     ->
     fail ;
     ask(S))).


undo :- retract(y(_)),fail.
undo :- retract(n(_)),fail.
undo.
```

### 4.2 Cómo ejecutar

```bash
# 1. Desde consola:
swipl cesareas.pl

# 2. Dentro del intérprete:
?- [cesareas].
?- identificar.
```

En cada pregunta responder `yes.` (o `y.`) / `no.` (o `n.`), seguido de punto.

---

## 5. Pruebas ejecutadas (resultados)

### 5.1 Corrida 1 — Cesárea prevista (bebé en posición podálica)

```text
?- identificar.

El caso presenta la siguiente característica : bebe_esta_en_posicion_podalica? yes.

Pienso que la cesárea es de tipo : cesárea prevista de antemano
La incisión a realizar es : transversal baja o de Joel Coell

Información sobre el tipo de incisión :
  - Transversal baja : es horizontal, la cicatriz no es visible.
  - De Joel Coell : es horizontal.

Fases de la intervención (siempre en este orden) :
  1) Cortar.
  2) Extraer al niño.
  3) Extraer la placenta.
  4) Suturar la herida.
true.
```

![[capturas/corrida1_prevista.png]]

### 5.2 Corrida 2 — Cesárea prevista (madre con diabetes gravídica)

```text
?- identificar.

El caso presenta la siguiente característica : bebe_esta_en_posicion_podalica? no.
El caso presenta la siguiente característica : la_madre_padece_gestosis? no.
El caso presenta la siguiente característica : la_madre_padece_diabetes_gravida? yes.

Pienso que la cesárea es de tipo : cesárea prevista de antemano
La incisión a realizar es : transversal baja o de Joel Coell

Información sobre el tipo de incisión :
  - Transversal baja : es horizontal, la cicatriz no es visible.
  - De Joel Coell : es horizontal.

Fases de la intervención (siempre en este orden) :
  1) Cortar.
  2) Extraer al niño.
  3) Extraer la placenta.
  4) Suturar la herida.
true.
```

![[capturas/corrida2_diabetes.png]]

### 5.3 Corrida 3 — Cesárea improvisada con incisión umbílico-púbica

```text
?- identificar.

El caso presenta la siguiente característica : bebe_esta_en_posicion_podalica? no.
El caso presenta la siguiente característica : la_madre_padece_gestosis? no.
El caso presenta la siguiente característica : la_madre_padece_diabetes_gravida? no.
El caso presenta la siguiente característica : placenta_esta_en_posicion_previa_central? no.
El caso presenta la siguiente característica : la_madre_tiene_problemas_de_corazon? no.
El caso presenta la siguiente característica : la_madre_tiene_problemas_renales? no.
El caso presenta la siguiente característica : la_madre_tiene_infecciones_en_vias_genitales? no.
El caso presenta la siguiente característica : cabeza_del_bebe_es_demasiado_grande? yes.
El caso presenta la siguiente característica : la_placenta_se_desprende? yes.

Pienso que la cesárea es de tipo : cesárea improvisada durante el parto
La incisión a realizar es : umbílico-púbica

Información sobre el tipo de incisión :
  - Es vertical, empieza debajo del ombligo y termina en el pubis.
  - La cicatriz es visible y grande.

Fases de la intervención (siempre en este orden) :
  1) Cortar.
  2) Extraer al niño.
  3) Extraer la placenta.
  4) Suturar la herida.
true.
```

![[capturas/corrida3_umbilicopubica.png]]

### 5.4 Corrida 4 — Cesárea improvisada con incisión transversal baja / Joel Coell

```text
?- identificar.

El caso presenta la siguiente característica : bebe_esta_en_posicion_podalica? no.
El caso presenta la siguiente característica : la_madre_padece_gestosis? no.
El caso presenta la siguiente característica : la_madre_padece_diabetes_gravida? no.
El caso presenta la siguiente característica : placenta_esta_en_posicion_previa_central? no.
El caso presenta la siguiente característica : la_madre_tiene_problemas_de_corazon? no.
El caso presenta la siguiente característica : la_madre_tiene_problemas_renales? no.
El caso presenta la siguiente característica : la_madre_tiene_infecciones_en_vias_genitales? no.
El caso presenta la siguiente característica : cabeza_del_bebe_es_demasiado_grande? no.
El caso presenta la siguiente característica : cabeza_del_bebe_no_esta_encajada? no.
El caso presenta la siguiente característica : ritmo_cardiaco_del_bebe_es_irregular? yes.
El caso presenta la siguiente característica : bebe_expulsa_meconio? yes.
El caso presenta la siguiente característica : la_placenta_se_desprende? no.

Pienso que la cesárea es de tipo : cesárea improvisada durante el parto
La incisión a realizar es : transversal baja o de Joel Coell

Información sobre el tipo de incisión :
  - Transversal baja : es horizontal, la cicatriz no es visible.
  - De Joel Coell : es horizontal.

Fases de la intervención (siempre en este orden) :
  1) Cortar.
  2) Extraer al niño.
  3) Extraer la placenta.
  4) Suturar la herida.
true.
```

![[capturas/corrida4_transversal.png]]

### 5.5 Resumen de los casos probados

| Corrida | Respuestas clave | Diagnóstico (cesárea) | Incisión |
|:---:|:---:|:---:|:---:|
| 1 | posición podálica = sí | prevista de antemano | transversal baja o Joel Coell |
| 2 | diabetes gravídica = sí | prevista de antemano | transversal baja o Joel Coell |
| 3 | cabeza grande = sí, placenta desprendida = sí | improvisada durante el parto | umbílico-púbica |
| 4 | sufrimiento fetal = sí, placenta desprendida = no | improvisada durante el parto | transversal baja o Joel Coell |

> Nota: `undo/0` limpia los hechos `y/1` y `n/1` al finalizar cada corrida, dejando la base de conocimiento lista para la siguiente consulta.

---

## 6. Referencias

1. World Health Organization (WHO). *WHO statement on caesarean section rates*. Ginebra: WHO; 2015. WHO/RHR/15.02. Disponible en: https://www.who.int/publications/i/item/WHO-RHR-15.02
2. Hofmeyr GJ, Mathai M, Shah A, Novikova N. *Techniques for caesarean section*. Cochrane Database Syst Rev. 2008;(1):CD004662. DOI: 10.1002/14651858.CD004662.pub2
3. National Institute for Health and Care Excellence (NICE). *Caesarean birth*. NICE guideline NG192. Londres: NICE; 2021 (actualizado). Disponible en: https://www.nice.org.uk/guidance/ng192
4. Gray C, Shanahan M. *Breech Presentation*. StatPearls [Internet]. Treasure Island (FL): StatPearls Publishing; 2026. Bookshelf ID: NBK448063. Disponible en: https://www.ncbi.nlm.nih.gov/books/NBK448063/
5. Oyelese Y, Smulian JC. *Placenta previa, placenta accreta, and vasa previa*. Obstet Gynecol. 2006;107(4):927-941.
6. Mylonas I, Friese K. *Indications for and Risks of Elective Cesarean Section*. Dtsch Arztebl Int. 2015;112(29-30):489-495.
7. Mathai M, Hofmeyr GJ, Mathai NE. *Abdominal surgical incisions for caesarean section*. Cochrane Database Syst Rev. 2021;(8):CD004453. DOI: 10.1002/14651858.CD004453.pub3