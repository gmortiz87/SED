import pandas as pd

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
