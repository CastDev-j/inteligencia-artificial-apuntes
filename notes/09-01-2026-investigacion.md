# Investigación: Éxitos de Sistemas Expertos Deterministas

Un **sistema experto determinista** es aquel que, ante la misma entrada, siempre produce la misma salida: su razonamiento se basa en reglas fijas SI-ENTONCES sin componentes aleatorios ni probabilísticos. Estos sistemas fueron los grandes éxitos de la IA simbólica entre 1965 y 1990.

---

## 1. DENDRAL (1965)

| | |
|---|---|
| **Creadores** | Edward Feigenbaum, Bruce Buchanan y Joshua Lederberg (Universidad de Stanford) |
| **Dominio** | Química orgánica |
| **Función** | Inferir la estructura molecular de compuestos orgánicos a partir de datos de espectrometría de masas |

### Resultados

Fue el primer sistema experto usado con **propósitos reales** fuera de la investigación. Los químicos y biólogos lo usaron durante aproximadamente 10 años para facilitar la inferencia de estructuras moleculares. Se convirtió en modelo a seguir para los sistemas expertos posteriores (MYCIN, PROSPECTOR y XCON derivaron de su enfoque).

### Referencias

- Lindsay, R., Buchanan, B. G., Feigenbaum, E. A., & Lederberg, J. (1980). *Applications of Artificial Intelligence for Organic Chemistry: The DENDRAL Project*. McGraw-Hill.
- Buchanan, B. G., & Feigenbaum, E. A. (1978). "Heuristic DENDRAL: A Program for Generating Explanatory Hypotheses in Organic Chemistry". *Machine Intelligence*, vol. 4.
- Wikipedia: *Dendral*. https://en.wikipedia.org/wiki/Dendral

---

## 2. MYCIN (1970s)

| | |
|---|---|
| **Creadores** | Edward Shortliffe (Universidad de Stanford) |
| **Dominio** | Medicina |
| **Función** | Diagnosticar enfermedades infecciosas de la sangre y recomendar antibióticos personalizados |

### Resultados

Con ~500 reglas IF-THEN y **encadenamiento hacia atrás**, MYCIN alcanzó una **tasa de aciertos del 65%**, mejor que la mayoría de los médicos no especialistas (80% en expertos del campo). Fue pionero en:
- Factores de certeza para manejar incertidumbre
- Módulo de explicación (justificaba cada diagnóstico)
- Recetar dosis personalizadas según peso, estatura, etc.

Aunque nunca se usó clínicamente por razones éticas y legales, su arquitectura dio origen a los "shells" de sistemas expertos (EMYCIN).

### Referencias

- Shortliffe, E. H. (1976). *Computer-Based Medical Consultations: MYCIN*. Elsevier.
- Buchanan, B. G., & Shortliffe, E. H. (1984). *Rule-Based Expert Systems: The MYCIN Experiments of the Stanford Heuristic Programming Project*. Addison-Wesley.
- Wikipedia: *Mycin*. https://es.wikipedia.org/wiki/Mycin

---

## 3. XCON / R1 (1978–1980s)

| | |
|---|---|
| **Creadores** | John McDermott (Carnegie Mellon) + DEC |
| **Dominio** | Configuración de computadoras |
| **Función** | Configurar pedidos de computadoras VAX validando compatibilidad de componentes |

### Resultados

Fue el primer sistema experto que demostró **rentabilidad comercial real**:
- Usaba **encadenamiento hacia adelante** y reglas de producción
- La base de reglas creció de ~750 (1980) a **más de 10,000** (hacia 1989)
- Para 1986 había procesado **80,000 pedidos anualmente** con una precisión del **95–98%**
- Ahorro estimado: **$25–40 millones de dólares al año**

Su impacto fue tan grande que lanzó la industria de los sistemas expertos: hacia 1985 las empresas gastaban más de **$1,000 millones al año** en esta tecnología.

### Referencias

- McDermott, J. (1982). "R1: A Rule-Based Configurer of Computer Systems". *Artificial Intelligence*, 19(1), 39–88.
- Barker, V. E., & O'Connor, D. E. (1989). "Expert Systems for Configuration at Digital: XCON and Beyond". *Communications of the ACM*.
- Wikipedia: *XCON*. https://en.wikipedia.org/wiki/XCON

---

## 4. PROSPECTOR (1970s–1980s)

| | |
|---|---|
| **Creadores** | Peter Hart, Richard Duda (SRI International, para el U.S. Geological Survey) |
| **Dominio** | Geología / exploración minera |
| **Función** | Evaluar la probabilidad de depósitos minerales y recomendar dónde perforar |

### Resultados

Es el caso más documentado de un sistema experto que generó un **descubrimiento real**: predijo la existencia de un **yacimiento de molibdeno desconocido** en el Monte Tolman (Washington, EE. UU.). El sistema:
- Usaba redes de reglas de inferencia combinadas con **encadenamiento hacia adelante y hacia atrás**
- Razonaba sobre datos geológicos incompletos e inciertos
- Fue verificado por la revista *Science* en un artículo de 1982 que confirmó el hallazgo

### Referencias

- Campbell, A. N., Hollister, V. F., Duda, R. O., & Hart, P. E. (1982). "Recognition of a Hidden Mineral Deposit by an Artificial Intelligence Program". *Science*, 217(4563), 927–929.
- Duda, R. O., Hart, P. E., & Einaudi, M. T. (1978). "PROSPECTOR—A Computer-Based Consultation System for Mineral Exploration". *Journal of the International Association for Mathematical Geology*, 10(5), 589–610.
- SRI International. *PROSPECTOR computer-based expert system*. https://www.sri.com/hoi/prospector-computer-based-expert-system

---

## 5. INTERNIST-I / CADUCEUS (1970s–1980s)

| | |
|---|---|
| **Creadores** | Harry Pople y Jack Myers (Universidad de Pittsburgh) |
| **Dominio** | Medicina interna |
| **Función** | Diagnóstico diferencial de enfermedades internas |

### Resultados

Fue descrito como el **sistema experto más intensivo en conocimiento** de su época:
- Predecessor INTERNIST-I: ~500 enfermedades y 3,550 manifestaciones (validado con casos de *New England Journal of Medicine*)
- CADUCEUS (1980s): capaz de diagnosticar hasta **1,000 enfermedades**
- Su base de conocimiento se construyó con años de entrevistas al doctor Jack Myers, uno de los mejores diagnosticadores de medicina interna
- Su conocimiento dio origen a QMR (*Quick Medical Reference*), un sistema de referencia clínica ampliamente adoptado

### Referencias

- Miller, R. A., Pople, H. E., & Myers, J. D. (1982). "INTERNIST-I: An Experimental Computer-Based Diagnostic Consultant for General Internal Medicine". *New England Journal of Medicine*, 307(8), 468–476.
- Pople, H. E. (1985). "Evolution of an Expert System: From INTERNIST to CADUCEUS". *Artificial Intelligence in Medicine*, 179–208.
- Wikipedia: *CADUCEUS (expert system)*. https://en.wikipedia.org/wiki/CADUCEUS_(expert_system)

---

## Resumen comparativo

| Sistema | Año | Dominio | Resultado destacado |
|---|---|---|---|
| **DENDRAL** | 1965 | Química | Primer SE usado con propósitos reales |
| **MYCIN** | 1970s | Medicina | 65% de acierto; origen de los shells |
| **XCON/R1** | 1980s | Computación | $25–40M ahorrados al año, 95–98% precisión |
| **PROSPECTOR** | 1970s | Geología | Descubrió un yacimiento real de molibdeno |
| **CADUCEUS** | 1980s | Medicina | Diagnóstico de hasta 1,000 enfermedades |

> **Conclusión:** estos cinco sistemas probaron que la IA determinista basada en reglas podía superar a humanos no expertos, generar valor económico medible y hasta realizar descubrimientos reales. Su principal legado fue demostrar la viabilidad comercial de la IA… y revelar el "cuello de botella" de la adquisición de conocimiento que luego dio paso al aprendizaje automático.