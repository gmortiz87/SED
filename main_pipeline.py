import subprocess, time, sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

SCRIPTS = [
    ("Extracción", BASE_DIR / "main_extracción.py"),
    ("Transformación", BASE_DIR / "main_transform.py"),
    ("Control de calidad", BASE_DIR / "transformacion" / "control_calidad_staging.py"),
    ("Depuración avanzada", BASE_DIR / "transformacion" / "flujo_calidad_depuracion.py"),
]

def run_script(nombre, ruta):
    start = time.time()
    print(f"\n🚀 Ejecutando {nombre} ...")
    try:
        subprocess.run([sys.executable, str(ruta)], check=True)
        print(f"✅ {nombre} completado en {time.time() - start:.2f} segundos.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en {nombre}: {e}")

def main():
    print("=== PIPELINE ETL COMPLETO ===")
    inicio = time.time()

    for nombre, ruta in SCRIPTS:
        run_script(nombre, ruta)

    print(f"\n🎯 Pipeline finalizado en {time.time() - inicio:.2f} segundos.")

if __name__ == "__main__":
    main()
