import time
from excel_utils import extraer_datos

if __name__ == "__main__":
    start = time.time()

    ruta_excel = r"C:\Users\Adminstrador\Documents\3 - Ave Fenix\Propuesta\Seguimiento a Procesos y Proyectos de Calidad Educativa.xlsx"
    hoja = "ESTRATEGIAS"
    output_file = "outputs/Registros_Fuente_Estrategias.xlsx"

    df_datos = extraer_datos(ruta_excel, hoja)

    end = time.time()
    print(f"\n⏱️ Tiempo total de ejecución: {end - start:.2f} segundos")

    if not df_datos.empty:
        df_datos.to_excel(output_file, index=False)
        print(f"\n✅ Extracción finalizada. {len(df_datos)} registros exportados a '{output_file}'.")
        print("\n📊 Primeros registros:")
        print(df_datos.head())
    else:
        print("⚠️ No se encontraron datos válidos en la hoja.")
