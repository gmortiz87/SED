import time
import pandas as pd
from pathlib import Path

from transformacion import (
    transformar_poai_2024,
    transformar_poai_2025,
    transformar_estrategias,
    transformar_regalias,
)

BASE_DIR = Path(__file__).resolve().parents[0]
STAGING_DIR = BASE_DIR / "transformacion" / "staging"
STAGING_DIR.mkdir(parents=True, exist_ok=True)

def main():
    start = time.time()
    print("🧪 TEST: Transformaciones (POAI, Estrategias, Regalías)\n")

    resultados = []

    # --- POAI 2024 ---
    try:
        print("\n--- POAI 2024 ---")
        df_fuente, df_proy, df_act, df_ben = transformar_poai_2024.run()
        resultados.extend([
            {"Fuente": "POAI 2024", "Tabla": "Fuente", "Total Registros": len(df_fuente)},
            {"Fuente": "POAI 2024", "Tabla": "Proyectos", "Total Registros": len(df_proy)},
            {"Fuente": "POAI 2024", "Tabla": "Actividades", "Total Registros": len(df_act)},
            {"Fuente": "POAI 2024", "Tabla": "Beneficiarios", "Total Registros": len(df_ben)},
        ])
    except Exception as e:
        print(f"[ERROR] Transformación POAI 2024: {e}")

    # --- POAI 2025 ---
    try:
        print("\n--- POAI 2025 ---")
        df_fuente, df_proy, df_act, df_ben = transformar_poai_2025.run()
        resultados.extend([
            {"Fuente": "POAI 2025", "Tabla": "Fuente", "Total Registros": len(df_fuente)},
            {"Fuente": "POAI 2025", "Tabla": "Proyectos", "Total Registros": len(df_proy)},
            {"Fuente": "POAI 2025", "Tabla": "Actividades", "Total Registros": len(df_act)},
            {"Fuente": "POAI 2025", "Tabla": "Beneficiarios", "Total Registros": len(df_ben)},
        ])
    except Exception as e:
        print(f"[ERROR] Transformación POAI 2025: {e}")

    # --- Estrategias ---
    try:
        print("\n--- Estrategias ---")
        df_fuente, df_proy, df_act, df_ben = transformar_estrategias.run()
        resultados.extend([
            {"Fuente": "Estrategias", "Tabla": "Fuente", "Total Registros": len(df_fuente)},
            {"Fuente": "Estrategias", "Tabla": "Proyectos", "Total Registros": len(df_proy)},
            {"Fuente": "Estrategias", "Tabla": "Actividades", "Total Registros": len(df_act)},
            {"Fuente": "Estrategias", "Tabla": "Beneficiarios", "Total Registros": len(df_ben)},
        ])
    except Exception as e:
        print(f"[ERROR] Transformación Estrategias: {e}")

    # --- Regalías ---
    try:
        print("\n--- Regalías ---")
        df_fuente, df_proy, df_act, df_ben = transformar_regalias.run()
        resultados.extend([
            {"Fuente": "Regalías", "Tabla": "Fuente", "Total Registros": len(df_fuente)},
            {"Fuente": "Regalías", "Tabla": "Proyectos", "Total Registros": len(df_proy)},
            {"Fuente": "Regalías", "Tabla": "Actividades", "Total Registros": len(df_act)},
            {"Fuente": "Regalías", "Tabla": "Beneficiarios", "Total Registros": len(df_ben)},
        ])
    except Exception as e:
        print(f"[ERROR] Transformación Regalías: {e}")

    end = time.time()

    # --- Resumen final en consola ---
    print("\n📊 RESUMEN DE REGISTROS GENERADOS:")
    for r in resultados:
        print(f"   - {r['Fuente']} | {r['Tabla']}: {r['Total Registros']} registros")

    print(f"\n✅ Test completado en {end - start:.2f} segundos.")

    # --- Guardar resumen en Excel ---
    resumen_df = pd.DataFrame(resultados)
    resumen_file = STAGING_DIR / "resumen_transformacion.xlsx"
    resumen_df.to_excel(resumen_file, index=False)

    print(f"\n💾 Resumen guardado en: {resumen_file}")


if __name__ == "__main__":
    main()
