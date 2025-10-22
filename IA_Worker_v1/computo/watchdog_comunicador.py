import time
import os
import subprocess
import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# --- Rutas del Cerebro y Cómputo ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # Apunta a IA_Worker/
CEREBRO_DIR = os.path.join(BASE_DIR, 'cerebro')
COMPUTO_DIR = os.path.join(BASE_DIR, 'computo')

# Archivo que el watchdog vigila
GEMINI_A_PYTHON_PATH = os.path.join(CEREBRO_DIR, 'gemini_a_python.json')

# Script que el watchdog ejecuta
CALCULADOR_SCRIPT_PATH = os.path.join(COMPUTO_DIR, 'calculador_ambiguedad.py')

class GeminiMessageHandler(FileSystemEventHandler):
    """
    Manejador de eventos que reacciona a los mensajes de Gemini.
    Su única responsabilidad es llamar al script calculador.
    """
    def on_modified(self, event):
        if not event.is_directory and event.src_path == GEMINI_A_PYTHON_PATH:
            print(f"👀 Detectado mensaje de Gemini. Disparando el calculador de métricas...")
            try:
                # Llama al script calculador como un proceso separado,
                # pasándole el archivo de entrada como argumento.
                subprocess.run(
                    [sys.executable, CALCULADOR_SCRIPT_PATH, "--input", GEMINI_A_PYTHON_PATH],
                    check=True
                )
            except subprocess.CalledProcessError as e:
                print(f"❌ Error al ejecutar el calculador: {e}")

if __name__ == "__main__":
    print(f"🛰️  Watchdog Comunicador iniciado. Escuchando cambios en '{os.path.basename(GEMINI_A_PYTHON_PATH)}'...")
    print("Presiona CTRL+C para detener.")
    
    event_handler = GeminiMessageHandler()
    observer = Observer()
    observer.schedule(event_handler, path=CEREBRO_DIR, recursive=False)
    
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    print("\n👋 Watchdog detenido.")