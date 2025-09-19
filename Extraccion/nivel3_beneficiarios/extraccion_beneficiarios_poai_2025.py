import time
import openpyxl
import pandas as pd
from utils.beneficiarios_utils import procesar_beneficiarios

if __name__ == "__main__":
    start = time.time()
    ruta_excel = r"C:\Users\Adminstrador\Documents\3 - Ave Fenix\Propuesta\Seguimiento a Procesos y Proyectos de Calidad Educativa.xlsx"

    hojas = [
        "Juegos_Ben_2025", "Gestion_Escolar_Ben_2025", "Convivencia_Ben_2025",
        "Educacion_Inicial_Ben_2025", "Articulacion_Ben_2025", "Normales_Ben_2025",
        "PEER_Ben_2025", "PILEO_Ben_2025", "Familia_Escuela_Ben_2025",
        "SEIP_Ben_2025", "AFRO_Ben_2025", "ADULTOS_Ben_2025",
        "PADRINAZGO_Ben_2025", "BIBLIOTECA_Ben_2025"
    ]

    wb = openpyxl.load_workbook(ruta_excel, data_only=True)
    dfs = []

    for hoja in hojas:
        if hoja in wb.sheetnames:
            ws = wb[hoja]
            df = procesar_beneficiarios(ws, hoja)
            if not df.empty:
                dfs.append(df)
        else:
            print(f"❌ La hoja {hoja} no existe en el archivo.")

    if dfs:
        df_total = pd.concat(dfs, ignore_index=True)
        end = time.time()
        print(f"\n✅ POAI 2025: {len(df_total)} registros procesados en {end - start:.2f} seg")
        print(df_total.head())

        output_file = "outputs/Registro_Beneficiarios_POAI_2025.xlsx"
        df_total.to_excel(output_file, index=False)
        print(f"📂 Archivo exportado: {output_file}")
    else:
        print("⚠️ No se encontraron datos válidos.")
