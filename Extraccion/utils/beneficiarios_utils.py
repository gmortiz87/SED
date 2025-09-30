"""import pandas as pd

def procesar_beneficiarios(ws, hoja_nombre):
    header_row = None
    for r in range(1, 20):
        if ws.cell(row=r, column=2).value == "N°":
            header_row = r
            break

    if not header_row:
        print(f"No se encontró cabecera en {hoja_nombre}")
        return pd.DataFrame()

    headers = []
    for c in range(2, ws.max_column+1):
        val = ws.cell(row=header_row, column=c).value
        if val:
            headers.append(str(val).strip())

    data = []
    for r in range(header_row+1, ws.max_row+1):
        row_vals, empty_row = [], True
        for c in range(2, 2+len(headers)):
            v = ws.cell(row=r, column=c).value
            row_vals.append(v)
            if v not in (None, ""):
                empty_row = False
        if empty_row:
            break
        data.append(row_vals)

    df = pd.DataFrame(data, columns=headers)
    df["Hoja"] = hoja_nombre
    return df
"""

import pandas as pd

# Lista negra de cabeceras que se deben eliminar
COLUMNAS_INVALIDAS = {"FUENTES", "PROYECTOS", "BENEFICIARIOS"}

def procesar_beneficiarios(ws, hoja_nombre):
    """
    Procesa una hoja de Excel con datos de beneficiarios.
    - Detecta la fila de cabecera buscando la celda 'N°'.
    - Construye el DataFrame.
    - Filtra columnas inválidas (ruido).
    - Captura hipervínculos si existen.
    """
    # === Buscar cabecera (fila con 'N°') ===
    header_row = None
    for r in range(1, 20):
        if ws.cell(row=r, column=2).value == "N°":
            header_row = r
            break

    if not header_row:
        print(f"[ALERTA] No se encontró cabecera en {hoja_nombre}")
        return pd.DataFrame()

    # === Construir cabeceras ===
    headers = []
    for c in range(2, ws.max_column + 1):
        val = ws.cell(row=header_row, column=c).value
        if val:
            headers.append(str(val).strip())

    # === Construir datos ===
    data = []
    for r in range(header_row + 1, ws.max_row + 1):
        row_vals, empty_row = [], True
        for c in range(2, 2 + len(headers)):
            cell = ws.cell(row=r, column=c)
            # Si hay hipervínculo, lo guardamos; si no, el valor normal
            v = cell.hyperlink.target if cell.hyperlink else cell.value
            row_vals.append(v)
            if v not in (None, ""):
                empty_row = False
        if empty_row:
            break
        data.append(row_vals)

    # === Armar DataFrame ===
    df = pd.DataFrame(data, columns=headers)

    # === Filtrar columnas inválidas ===
    columnas_validas = [
        col for col in df.columns
        if col and not col.startswith("Unnamed")
        and col not in COLUMNAS_INVALIDAS
    ]
    df = df[columnas_validas]

    # === Agregar columna de trazabilidad ===
    df["Hoja"] = hoja_nombre

    return df
