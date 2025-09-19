# utils/proyectos_helpers.py
import re
import pandas as pd

def find_row_contains(ws, pattern, start_row=1, end_row=200):
    """
    Busca la primera fila en una hoja de Excel que contenga un patrón de texto.
    Devuelve el número de fila o None si no se encuentra.
    """
    regex = re.compile(pattern, re.IGNORECASE)
    for row in range(start_row, end_row + 1):
        for cell in ws[row]:
            if cell.value and regex.search(str(cell.value)):
                return row
    return None


def extraer_actividades(ws, hoja, col_idx, columnas, r_title, r_obs, data_start):
    """
    Extrae las actividades de una hoja de Excel en formato tabular.
    Incluye Observaciones Generales como columna adicional (si existe).
    
    Parámetros:
    - ws: hoja de trabajo de openpyxl
    - hoja: nombre de la hoja procesada
    - col_idx: índices de columnas (1-based, como Excel)
    - columnas: nombres de las columnas
    - r_title: fila donde empieza la sección ACTIVIDADES
    - r_obs: fila donde aparece Observaciones Generales
    - data_start: fila donde empiezan los datos después del encabezado
    """
    data = []

    # Determinar hasta qué fila leer (incluyendo observaciones si existen)
    max_row = r_obs or ws.max_row

    for row in ws.iter_rows(min_row=data_start, max_row=max_row, values_only=True):
        if row and any(row):  # ignorar filas completamente vacías
            fila = [row[i - 1] if (i - 1) < len(row) else None for i in col_idx]
            data.append(fila)

    # Crear DataFrame con los encabezados correctos
    df = pd.DataFrame(data, columns=columnas)

    # Añadir la hoja como metadato
    df["Hoja"] = hoja

    # Filtrar posibles filas que capturen el título "Observaciones Generales"
    if "Actividad del Proyecto" in df.columns:
        df = df[df["Actividad del Proyecto"] != "Observaciones Generales"]

    return df
