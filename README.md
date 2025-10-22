# IA_Worker
En este repositorio estamos trabajando en como podemos crear una memoria de un proyecto a una IA, ademas de como podemos sesgar a la IA usando estadistica y python., aprovechando las herramientas que ofrece la IA

## Version 1: 

Esta primera versión se centra en establecer un sistema de comunicación robusto y autoanalítico que minimiza la ambigüedad y maximiza la eficiencia.

--> Comunicación Asíncrona a través de un "Cerebro" Central: La comunicación entre Gemini y los scripts de Python se gestiona a través de un directorio cerebro/. Gemini deja sus "órdenes" en formato JSON (gemini_a_python.json), y un script de Python (watchdog_comunicador.py) detecta los cambios y activa los procesos de análisis.

--> Análisis Predictivo de Ambigüedad: El corazón del sistema es el calculador_ambiguedad.py. Este script no solo mide la proporción de tareas "claras" vs. "ambiguas" en un momento dado, sino que utiliza una regresión lineal para analizar el historial de interacciones. Esto le permite calcular una pendiente que predice si la comunicación está mejorando o empeorando con el tiempo.

--> Modos de Operación Reactivos: Basándose en las métricas de ambigüedad y en la pendiente de la regresión, la IA opera en dos modos distintos para adaptarse a la situación:

-----> Modo Preguntas: Si la ambigüedad supera el 30% o la pendiente es mayor a 0.1 (indicando una tendencia a la confusión), la IA se detiene y se enfoca exclusivamente en hacer preguntas para aclarar los requisito

-----> Modo Ejecución: Cuando la comunicación es fluida (ambigüedad <= 30% y pendiente <= 0.1), la IA procede con la ejecución de las tareas planificadas sin interrumpir el flujo de trabajo.

--> Gestión de Carga de Trabajo: El sistema también evalúa la complejidad total de las tareas y advierte al usuario si la carga de trabajo es demasiado alta, sugiriendo dividir los módulos para una mejor gestión.

