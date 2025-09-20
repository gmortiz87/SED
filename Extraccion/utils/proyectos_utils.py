# utils/proyectos_utils.py
import openpyxl
import pandas as pd
from pathlib import Path
import re

def find_row_contains(ws, pattern, start_row=1, end_row=200):
    """
    Busca la primera fila en una hoja de Excel que contenga un patrón de texto.
    """
    regex = re.compile(pattern, re.IGNORECASE)
    for row in range(start_row, end_row + 1):
        for cell in ws[row]:
            if cell.value and regex.search(str(cell.value)):
                return row
    return None


def procesar_fuente_proyectos(ruta_excel, fuente, hojas, output_file):
    """
    Procesa proyectos y actividades para una fuente dada (POAI, ESTRATEGIAS, REGALIAS).
    - Extrae proyectos y actividades.
    - Incluye Observaciones Generales como columna.
    - Incluye columna de URL de evidencias.
    Exporta un archivo Excel en extraccion/outputs/.
    """
    wb = openpyxl.load_workbook(ruta_excel, data_only=True)
    proyectos, actividades_total = [], []

    for hoja in hojas:
        if hoja not in wb.sheetnames:
            print(f"[ALERTA] La hoja {hoja} no existe en el archivo.")
            continue

        ws = wb[hoja]

        # --- Metadatos del proyecto según la fuente ---
        if fuente.upper().startswith("POAI") or fuente.upper() == "REGALIAS":
            info_proyecto = {
                "Nombre del Proyecto": ws["D3"].value,
                "Vigencia": ws["D4"].value,
                "Código BPIN": ws["F4"].value,
                "Código PI": ws["H4"].value,
                "Total Ejecutado": ws["J4"].value,
                "RECURSOS": ws["L4"].value,
                "Hoja": hoja
            }
        elif fuente.upper() == "ESTRATEGIAS":
            info_proyecto = {
                "Nombre de la Estrategia": ws["D3"].value,
                "Hoja": hoja
            }
        else:
            info_proyecto = {
                "Nombre": ws["D3"].value,
                "Hoja": hoja
            }

        # --- Localizar secciones ---
        r_title = find_row_contains(ws, r"ACTIVIDADES", 1, 200)
        header_row = (r_title or 0) + 1
        data_start = header_row + 1
        r_obs = find_row_contains(ws, r"Observaciones\s+Generales", start_row=data_start, end_row=500)

        # --- Extraer actividades ---
        col_idx = [2, 3, 6, 7, 8, 9, 10, 11, 12]
        columnas = [
            "N°", "Actividad del Proyecto", "Total Ejecutado",
            "Componente PAM", "¿A qué actor va dirigida?",
            "Número de Beneficiarios", "Entrega Dotación (SI / NO)",
            "Descripción de la Dotación Entregada", "Evidencia de la Actividad"
        ]

        data = []
        row = data_start
        last_row = (r_obs - 1) if r_obs else ws.max_row

        while row <= last_row:
            values = [ws.cell(row=row, column=i).value for i in col_idx]

            # Extraer URL de evidencia si existe
            evidencia_cell = ws.cell(row=row, column=12)
            evidencia_url = evidencia_cell.hyperlink.target if evidencia_cell.hyperlink else None

            fila = values + [evidencia_url]
            if any(fila):
                data.append(fila)
            row += 1

        df_actividades = pd.DataFrame(data, columns=columnas + ["Evidencia_URL"])

        # --- Agregar Observaciones Generales ---
        if r_obs:
            obs_parts = []
            for col in range(5, 13):  # rango donde suelen estar observaciones
                v = ws.cell(row=r_obs, column=col).value
                if v not in (None, ""):
                    obs_parts.append(str(v).strip())
            observacion_final = " | ".join(obs_parts).strip() if obs_parts else "Sin observaciones"
        else:
            observacion_final = "Sin observaciones"

        df_actividades["Observaciones Generales"] = observacion_final

        # --- Limpieza de encabezados falsos ---
        if not df_actividades.empty and isinstance(df_actividades.iloc[0, 1], str) and "actividad" in df_actividades.iloc[0, 1].lower():
            df_actividades = df_actividades.iloc[1:].reset_index(drop=True)

        # --- Metadatos adicionales ---
        df_actividades["Hoja"] = hoja
        # Asignar nombre dinámico de acuerdo a la fuente
        if fuente.upper() == "ESTRATEGIAS":
            df_actividades["Nombre de la Estrategia"] = ws["D3"].value
        else:
            df_actividades["Nombre del Proyecto"] = ws["D3"].value

        proyectos.append(info_proyecto)
        actividades_total.append(df_actividades)

    # --- Crear DataFrames finales ---
    df_proyectos = pd.DataFrame(proyectos)
    actividades_total = [df for df in actividades_total if not df.empty]
    df_actividades = pd.concat(actividades_total, ignore_index=True) if actividades_total else pd.DataFrame()

    # --- Exportar resultados ---
    if not df_proyectos.empty or not df_actividades.empty:
        output_path = Path("extraccion/outputs") / output_file
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
            df_proyectos.to_excel(writer, sheet_name="Info_Proyectos", index=False)
            df_actividades.to_excel(writer, sheet_name="Actividades", index=False)

        print(f"[OK] {len(df_proyectos)} proyectos y {len(df_actividades)} actividades exportadas a {output_path}")
    else:
        print("[ALERTA] No se encontraron datos válidos.")

    return df_proyectos, df_actividades
