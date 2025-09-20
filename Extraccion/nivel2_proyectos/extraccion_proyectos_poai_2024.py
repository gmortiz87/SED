import time
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.config_fuentes import FUENTES_HOJAS
from utils.proyectos_utils import procesar_fuente_proyectos

def run(fuente="POAI_2024"):
    start = time.time()
    ruta_excel = r"C:\Users\Adminstrador\Documents\3 - Ave Fenix\Propuesta\Seguimiento a Procesos y Proyectos de Calidad Educativa.xlsx"
    hojas = FUENTES_HOJAS[fuente]

    df_proyectos, df_actividades = procesar_fuente_proyectos(
        ruta_excel,
        fuente,
        hojas,
        f"Registro_Proyectos_Actividades_{fuente}.xlsx"
    )

    end = time.time()

    print(f"[INFO] {len(df_proyectos)} proyectos y {len(df_actividades)} actividades exportadas")

    print("\n[OK] Primeros registros POAI 2024:")
    print(df_proyectos.head())
    
    print("\n[OK] Primeros registros actividades:")
    print(df_actividades.head())

    print(f"[TIEMPO] Extracción {fuente}: {end - start:.2f} segundos")

    return df_proyectos, df_actividades
