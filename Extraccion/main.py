import sys
import subprocess
import os

# Ruta base del proyecto
base_dir = r"C:\Users\Adminstrador\Documents\3 - Ave Fenix\Propuesta\Proyecto\extraccion"

# Python actual (del .venv)
python_exec = sys.executable

# Scripts por nivel
scripts = {
    "Nivel 1 - Fuente": [
        "nivel1_fuentes/extraccion_fuente_poai_2024.py",
        "nivel1_fuentes/extraccion_fuente_poai_2025.py",
        "nivel1_fuentes/extraccion_fuente_regalias.py",
        "nivel1_fuentes/extraccion_fuente_estrategias.py",
    ],
    "Nivel 2 - Proyectos/Actividades": [
        "nivel2_proyectos/extraccion_proyectos_poai_2024.py",
        "nivel2_proyectos/extraccion_proyectos_poai_2025.py",
        "nivel2_proyectos/extraccion_proyectos_regalias.py",
        "nivel2_proyectos/extraccion_proyectos_estrategia.py",
    ],
    "Nivel 3 - Beneficiarios": [
        "nivel3_beneficiarios/extraccion_beneficiarios_poai_2024.py",
        "nivel3_beneficiarios/extraccion_beneficiarios_poai_2025.py",
        "nivel3_beneficiarios/extraccion_beneficiarios_regalias.py",
        "nivel3_beneficiarios/extraccion_beneficiarios_estrategia.py",
    ],
}

# Ejecutar cada script
for nivel, lista in scripts.items():
    print("\n" + "=" * 30)
    print(f"   🚀 Ejecutando {nivel}")
    print("=" * 30)

    for script in lista:
        script_path = os.path.join(base_dir, script)
        print(f"\n🚀 Ejecutando {script_path} ...\n")
        try:
            result = subprocess.run([python_exec, script_path], capture_output=True, text=True)
            if result.returncode == 0:
                print(result.stdout)
            else:
                print("⚠️ Errores:")
                print(result.stderr)
        except Exception as e:
            print(f"❌ Error ejecutando {script}: {e}")

print("\n✅ Proceso ETL de extracción COMPLETADO con éxito.")
