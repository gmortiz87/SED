import time
import openpyxl
import pandas as pd
import sys, os
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.stdout.reconfigure(encoding="utf-8")

from utils.beneficiarios_utils import procesar_beneficiarios
from utils.export_utils import guardar_excel 
from utils.config_fuentes import FUENTES_HOJAS_BEN

OUTPUT_DIR = Path(__file__).resolve().parents[2] / "extraccion" / "outputs"

def run(fuente="REGALIAS"):
    start = time.time()
    ruta_excel = r"C:\Users\Adminstrador\Documents\3 - Ave Fenix\Propuesta\Seguimiento a Procesos y Proyectos de Calidad Educativa.xlsx"

    hojas = FUENTES_HOJAS_BEN.get(fuente, [])
    wb = openpyxl.load_workbook(ruta_excel, data_only=True)
    dfs = []

    for hoja in hojas:
        if hoja in wb.sheetnames:
            ws = wb[hoja]
            df = procesar_beneficiarios(ws, hoja)
            if not df.empty:
                dfs.append(df)
            else:
                print(f"[ALERTA] La hoja {hoja} no tiene datos válidos.")
        else:
            print(f"[ALERTA] La hoja {hoja} no existe en el archivo.")

    if dfs:
        df_total = pd.concat(dfs, ignore_index=True)
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        output_file = OUTPUT_DIR / f"Registro_Beneficiarios_{fuente}.xlsx"

        guardar_excel({"Beneficiarios": df_total}, output_file)
        print(f"[OK] {len(df_total)} beneficiarios exportados a {output_file}")

        print("\n[DATA] Primeros registros:")
        print(df_total.head())
    else:
        print("[ALERTA] No se encontraron datos válidos en ninguna hoja.")

    end = time.time()
    print(f"[TIEMPO] Extracción {fuente}: {end - start:.2f} segundos")
