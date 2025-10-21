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
    hoja = "REGALIAS"
    ruta_excel = r"C:\Users\Adminstrador\Documents\3 - Ave Fenix\Propuesta\Seguimiento a Procesos y Proyectos de Calidad Educativa.xlsx"
    
    df_datos = extraer_datos(ruta_excel, hoja)

    if not df_datos.empty:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        output_file = OUTPUT_DIR / "Registros_Fuente_Regalias.xlsx"    
        guardar_excel({hoja: df_datos}, output_file)

        print(f"\n📊 {len(df_datos)} registros exportados de la hoja {hoja}")
        print("\n✅ Primeros registros:")
        print("\n",df_datos.head())
    else:
        print("\n[ALERTA] No se encontraron datos válidos en la hoja.")

    end = time.time()
    print(f"\n[TIEMPO] Extracción Regalias: {end - start:.2f} segundos")
