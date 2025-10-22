import json
import os
import argparse
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime

# --- Rutas del Cerebro ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # Apunta a IA_Worker/
CEREBRO_DIR = os.path.join(BASE_DIR, 'cerebro')

# Archivo de salida para Gemini y archivo de estado para el historial
PYTHON_A_GEMINI_PATH = os.path.join(CEREBRO_DIR, 'python_a_gemini.json')
HISTORIAL_AMBIGUEDAD_PATH = os.path.join(CEREBRO_DIR, 'historial_ambiguedad.json')

def calcular_proporcion_y_complejidad(tareas_clasificadas):
    """Calcula la proporción de ambigüedad y la carga de trabajo total."""
    if not tareas_clasificadas:
        return 0.0, 0
    total_tareas = len(tareas_clasificadas)
    tareas_ambiguas = sum(1 for t in tareas_clasificadas if t.get('clasificacion') == 'ambigua')
    proporcion = round(tareas_ambiguas / total_tareas, 2)
    carga_trabajo = sum(t.get('complejidad', 3) for t in tareas_clasificadas)
    return proporcion, carga_trabajo

def actualizar_historial_y_regresion(nueva_proporcion):
    """Carga el historial, añade el nuevo dato y calcula la regresión lineal."""
    historial = []
    if os.path.exists(HISTORIAL_AMBIGUEDAD_PATH):
        with open(HISTORIAL_AMBIGUEDAD_PATH, 'r', encoding='utf-8') as f:
            try:
                historial = json.load(f).get('historial_proporciones', [])
            except json.JSONDecodeError:
                historial = []
    
    historial.append(nueva_proporcion)
    
    tendencia = {"pendiente": 0, "proyeccion_proxima_iteracion": nueva_proporcion}
    if len(historial) >= 2:
        iteraciones = np.array(range(len(historial))).reshape(-1, 1)
        proporciones = np.array(historial)
        model = LinearRegression().fit(iteraciones, proporciones)
        pendiente = model.coef_[0]
        proyeccion = model.predict(np.array([[len(historial)]]))[0]
        tendencia = {
            "pendiente": round(pendiente, 2),
            "proyeccion_proxima_iteracion": round(max(0, min(1, proyeccion)), 2)
        }
    
    # Guarda el historial actualizado para la próxima ejecución
    with open(HISTORIAL_AMBIGUEDAD_PATH, 'w', encoding='utf-8') as f:
        json.dump({"historial_proporciones": historial}, f, indent=2)

    return tendencia

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calcula métricas de ambigüedad de tareas clasificadas por Gemini.")
    parser.add_argument("--input", required=True, help="Ruta al archivo JSON de entrada con las tareas de Gemini.")
    args = parser.parse_args()

    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            data = json.load(f)
        tareas = data.get('tareas', [])
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"❌ Error al leer el archivo de entrada: {e}")
        exit(1)

    proporcion_actual, carga_trabajo_total = calcular_proporcion_y_complejidad(tareas)
    tendencia_regresion = actualizar_historial_y_regresion(proporcion_actual)

    # Sugerencia de carga de trabajo
    SUGERENCIA_CARGA = "La carga de trabajo para este módulo parece óptima."
    if carga_trabajo_total > 15:
        SUGERENCIA_CARGA = "ADVERTENCIA: La carga de trabajo es alta. Sugiero dividir este módulo en dos más pequeños."

    metricas_finales = {
        "timestamp": datetime.now().isoformat(),
        "proporcion_ambiguedad_actual": proporcion_actual,
        "tendencia_ambiguedad": tendencia_regresion,
        "carga_trabajo_total": carga_trabajo_total,
        "sugerencia_carga_trabajo": SUGERENCIA_CARGA
    }
    
    # Escribe el resultado final en el archivo de respuesta para Gemini
    with open(PYTHON_A_GEMINI_PATH, 'w', encoding='utf-8') as f:
        json.dump(metricas_finales, f, indent=2)

    print("✅ Respuesta para Gemini generada y guardada en python_a_gemini.json:")
    print(json.dumps(metricas_finales, indent=2))