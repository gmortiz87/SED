# ===============================================
# helpers_igp.py
# Utilidades para procesar hojas IGP (Nivel 4)
# ===============================================

import re
import pandas as pd


# -----------------------------------------------
# Limpieza de valores numéricos
# -----------------------------------------------
def limpiar_numero(valor):
    """
    Limpia un valor numérico que puede venir con comas o puntos,
    devolviendo un float o None si no es convertible.
    """
    if valor is None or str(valor).strip() == "":
        return None

    texto = str(valor).strip().replace(".", "").replace(",", ".")
    try:
        return float(texto)
    except ValueError:
        return None


# -----------------------------------------------
# Búsqueda de valores fijos en cabecera
# -----------------------------------------------
def buscar_valor(ws, etiqueta, rango=(1, 25)):
    """
    Busca un texto en la hoja y devuelve el valor de la celda adyacente.
    Útil para capturar COD. PI, COD. BPIN, NOMBRE PROYECTO, VIGENCIA, etc.
    """
    regex = re.compile(etiqueta, re.IGNORECASE)
    for r in range(rango[0], rango[1] + 1):
        for c in range(1, ws.max_column + 1):
            val = ws.cell(row=r, column=c).value
            if val and regex.search(str(val)):
                return ws.cell(row=r, column=c + 1).value
    return None


# -----------------------------------------------
# Extracción de bloque "CÓDIGO Y DESCRIPCIÓN DE MP"
# -----------------------------------------------
def extraer_bloque_metas(ws, hoja, fuente, cod_pi, cod_bpin, nombre_proyecto, vigencia):
    """
    Extrae las metas de producto (MP) desde el bloque 'CÓDIGO Y DESCRIPCIÓN DE MP'
    y sus valores asociados 'MP PROGRAMADA PARA' y 'AVANCE DE LA MP'.
    Permite varias metas por hoja.
    """
    data = []
    header_row = None

    # Buscar la fila donde inicia el bloque de MP
    for r in range(10, ws.max_row + 1):
        val = ws.cell(row=r, column=2).value
        if val and "CÓDIGO" in str(val).upper() and "MP" in str(val).upper():
            header_row = r
            break

    if not header_row:
        print(f"[AVISO] No se encontró bloque de MP en {hoja}")
        return pd.DataFrame()

    col_codigo = 2
    col_programada = col_codigo + 1
    col_avance = col_codigo + 2

    for r in range(header_row + 1, ws.max_row + 1):
        codigo_desc = ws.cell(row=r, column=col_codigo).value
        mp_prog = ws.cell(row=r, column=col_programada).value
        mp_avance = ws.cell(row=r, column=col_avance).value

        if not any([codigo_desc, mp_prog, mp_avance]):
            break

        codigo_mp, descripcion_mp = None, None
        if isinstance(codigo_desc, str):
            partes = codigo_desc.split("-", 1)
            codigo_mp = partes[0].strip() if len(partes) > 0 else None
            descripcion_mp = partes[1].strip() if len(partes) > 1 else None
        else:
            descripcion_mp = codigo_desc

        mp_prog_val = limpiar_numero(mp_prog)
        mp_avance_val = limpiar_numero(mp_avance)
        mp_porcentaje = None
        if mp_prog_val and mp_avance_val:
            try:
                mp_porcentaje = round((mp_avance_val / mp_prog_val) * 100, 2)
            except ZeroDivisionError:
                mp_porcentaje = None

        data.append({
            "Fuente": fuente,
            "Hoja": hoja,
            "COD_PI": cod_pi,
            "COD_BPIN": cod_bpin,
            "Nombre_Proyecto": nombre_proyecto,
            "Vigencia": vigencia,
            "CODIGO_MP": codigo_mp,
            "Descripcion_MP": descripcion_mp,
            "MP_Programada": mp_prog_val,
            "MP_Avance": mp_avance_val,
            "MP_Porcentaje": mp_porcentaje
        })

    return pd.DataFrame(data)


# -----------------------------------------------
# Extracción de bloque "NOMBRE DEL PRODUCTO"
# -----------------------------------------------
def extraer_bloque_productos(ws, hoja, fuente, cod_pi, cod_bpin, nombre_proyecto, vigencia):
    """
    Extrae el bloque de productos y sus indicadores, si existe.
    Este bloque inicia típicamente con 'NOMBRE DEL PRODUCTO'.
    """
    data = []
    header_row = None

    for r in range(10, ws.max_row + 1):
        val = ws.cell(row=r, column=3).value
        if val and "NOMBRE DEL PRODUCTO" in str(val).upper():
            header_row = r
            break

    if not header_row:
        return pd.DataFrame()

    for r in range(header_row + 1, ws.max_row + 1):
        nombre_producto = ws.cell(row=r, column=3).value
        indicador_producto = ws.cell(row=r, column=4).value
        unidad = ws.cell(row=r, column=5).value
        meta = ws.cell(row=r, column=6).value
        avance = ws.cell(row=r, column=7).value
        porc = ws.cell(row=r, column=8).value

        if not any([nombre_producto, indicador_producto, unidad, meta, avance, porc]):
            break

        data.append({
            "Fuente": fuente,
            "Hoja": hoja,
            "COD_PI": cod_pi,
            "COD_BPIN": cod_bpin,
            "Nombre_Proyecto": nombre_proyecto,
            "Vigencia": vigencia,
            "Nombre_Producto": nombre_producto,
            "Indicador_Producto": indicador_producto,
            "Unidad_Medida": unidad,
            "Meta_Vigente": limpiar_numero(meta),
            "Avance_Meta": limpiar_numero(avance),
            "Porcentaje_Avance": limpiar_numero(porc)
        })

    return pd.DataFrame(data)


# -----------------------------------------------
# Procesamiento completo de una hoja IGP
# -----------------------------------------------
def procesar_igp_hoja(ws, hoja, fuente):
    """
    Procesa una hoja completa IGP:
    - Captura cabecera (PI, BPIN, Proyecto, Vigencia)
    - Extrae bloque de metas (MP)
    - Extrae bloque de productos
    - Devuelve DataFrame combinado
    """
    cod_pi = buscar_valor(ws, r"COD.?PI")
    cod_bpin = buscar_valor(ws, r"COD.?BPIN")
    nombre_proyecto = buscar_valor(ws, r"NOMBRE\s+PROYECTO")
    vigencia = buscar_valor(ws, r"VIGENCIA")

    df_metas = extraer_bloque_metas(ws, hoja, fuente, cod_pi, cod_bpin, nombre_proyecto, vigencia)
    df_productos = extraer_bloque_productos(ws, hoja, fuente, cod_pi, cod_bpin, nombre_proyecto, vigencia)

    if df_metas.empty and df_productos.empty:
        return pd.DataFrame()

    if not df_metas.empty and not df_productos.empty:
        df_final = pd.merge(
            df_metas,
            df_productos,
            on=["Fuente", "Hoja", "COD_PI", "COD_BPIN", "Nombre_Proyecto", "Vigencia"],
            how="outer"
        )
    else:
        df_final = pd.concat([df_metas, df_productos], ignore_index=True)

    return df_final
