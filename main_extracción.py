# main.py
import time

# Nivel 1 - Fuentes
from extraccion.nivel1_fuentes import (
    extraccion_fuente_poai_2025,
    extraccion_fuente_poai_2024,
    extraccion_fuente_regalias,
    extraccion_fuente_estrategias
)

# Nivel 2 - Proyectos
from extraccion.nivel2_proyectos import (
    extraccion_proyectos_estrategia,
    extraccion_proyectos_poai_2024,
    extraccion_proyectos_poai_2025,
    extraccion_proyectos_regalias
)

# Nivel 3 - Beneficiarios
from extraccion.nivel3_beneficiarios import (
    extraccion_beneficiarios_estrategia,
    extraccion_beneficiarios_poai_2024,
    extraccion_beneficiarios_poai_2025,
    extraccion_beneficiarios_regalias
)

# Transformación
#from transformacion import unificar_fuente_proyecto_beneficiario

# Carga
#from carga import carga_datamart


def main():
    start = time.time()
    print("🚀 Iniciando pipeline ETL...\n")

    # ========================
    # 1. EXTRACCIÓN
    # ========================
    print("\n📥 Extrayendo Nivel 1 (Fuentes)...")
    extraccion_fuente_poai_2025.run()
    extraccion_fuente_poai_2024.run()
    extraccion_fuente_regalias.run()
    extraccion_fuente_estrategias.run()

    print("\n📥 Extrayendo Nivel 2 (Proyectos)...")
    extraccion_proyectos_estrategia.run()
    extraccion_proyectos_poai_2024.run()
    extraccion_proyectos_poai_2025.run()
    extraccion_proyectos_regalias.run()

    print("\n📥 Extrayendo Nivel 3 (Beneficiarios)...")
    extraccion_beneficiarios_estrategia.run()
    extraccion_beneficiarios_poai_2024.run()
    extraccion_beneficiarios_poai_2025.run()
    extraccion_beneficiarios_regalias.run()

    # ========================
    # 2. TRANSFORMACIÓN
    # ========================
    # print("\n🔄 Unificando fuentes, proyectos y beneficiarios...")
    # unificar_fuente_proyecto_beneficiario.run()

    # ========================
    # 3. CARGA
    # ========================
    # print("\n⬆️ Cargando al Data Mart...")
    # carga_datamart.run()

    # ========================
    # TIEMPO TOTAL
    # ========================
    end = time.time()
    print(f"\n✅ Pipeline finalizado en {end - start:.2f} segundos.")


if __name__ == "__main__":
    main()
