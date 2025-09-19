import re
import pandas as pd

def find_row_contains(ws, pattern, start_row=1, end_row=500):
    pat = re.compile(pattern, re.IGNORECASE)
    for r in range(start_row, end_row+1):
        for c in ws.iter_cols(min_row=r, max_row=r):
            val = c[0].value
            if val and pat.search(str(val)):
                return r
    return None

def row_all_none(ws, row, cols):
    return all(ws.cell(row=row, column=c).value is None for c in cols)

def extraer_actividades(ws, hoja_nombre, col_idx, columnas_actividades, r_title, r_obs, data_start=0):
    actividades = []
    r = data_start
    last_row = (r_obs - 1) if r_obs else 500
    while r <= last_row:
        if row_all_none(ws, r, col_idx):
            break
        fila = [ws.cell(row=r, column=c).value for c in col_idx]
        actividades.append(fila)
        r += 1

    df = pd.DataFrame(actividades, columns=columnas_actividades)

    # Eliminar encabezado duplicado
    if not df.empty and isinstance(df.iloc[0, 1], str) and "actividad" in df.iloc[0, 1].lower():
        df = df.iloc[1:].reset_index(drop=True)

    # Hipervínculos en columna 12 (L)
    evidencia_urls = []
    r_data_start = data_start + 1 if r_title and not df.empty else data_start
    for i in range(len(df)):
        cell = ws.cell(row=r_data_start + i, column=12)
        evidencia_urls.append(cell.hyperlink.target if cell.hyperlink else None)
    df["Evidencia_URL"] = evidencia_urls

    # Observaciones
    if r_obs:
        obs_parts = []
        for col in range(5, 13):  # E..L
            v = ws.cell(row=r_obs, column=col).value
            if v not in (None, ""):
                obs_parts.append(str(v).strip())
        observacion_final = " | ".join(obs_parts).strip() if obs_parts else "Sin observaciones"
    else:
        observacion_final = "Sin observaciones"
    df["Observaciones Generales"] = observacion_final

    df["Hoja"] = hoja_nombre
    return df
