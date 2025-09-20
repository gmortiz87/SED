# extraccion/nivel1_fuentes/extraccion_fuente_estrategias_2025.py
import time
import sys, os
from pathlib import Path

# Ajustar paths para importar utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.excel_utils import extraer_datos
from utils.export_utils import guardar_excel

# OUTPUT_DIR = Path("extraccion/outputs")
OUTPUT_DIR = Path(__file__).resolve().parents[2] / "extraccion" / "outputs"


def run():
    start = time.time()
    hoja = "ESTRATEGIAS"
    ruta_excel = r"C:\Users\Adminstrador\Documents\3 - Ave Fenix\Propuesta\Seguimiento a Procesos y Proyectos de Calidad Educativa.xlsx"
    
    df_datos = extraer_datos(ruta_excel, hoja)

    if not df_datos.empty:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        output_file = OUTPUT_DIR / "Registros_Fuente_Estrategias.xlsx"
        guardar_excel({hoja: df_datos}, output_file)

        print(f"[INFO] {len(df_datos)} registros exportados de la hoja {hoja}")
        print("\n[OK] Primeros registros:")
        print(df_datos.head())
    else:
        print("[ALERTA] No se encontraron datos válidos en la hoja.")

    end = time.time()
    print(f"[TIEMPO] Extracción Estrategias: {end - start:.2f} segundos")
