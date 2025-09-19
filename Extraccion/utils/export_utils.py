import os
import pandas as pd

def get_output_path(filename: str) -> str:
    """
    Retorna la ruta absoluta al archivo dentro de extraccion/outputs,
    sin importar desde dónde se ejecute el script.
    """
    # Ubicar carpeta base del proyecto (extraccion/)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(base_dir, "outputs")
    os.makedirs(output_dir, exist_ok=True)  # crea la carpeta si no existe

    return os.path.join(output_dir, filename)


def guardar_excel(dataframes: dict, filename: str):
    """
    Guarda uno o varios DataFrames en un archivo Excel dentro de extraccion/outputs.

    Parámetros:
        dataframes (dict): nombre_hoja -> DataFrame
        filename (str): nombre del archivo de salida (ej: 'resultado.xlsx')
    """
    output_file = get_output_path(filename)

    with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
        for sheet_name, df in dataframes.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)

    print(f"[OK] Archivo exportado: {output_file}")
