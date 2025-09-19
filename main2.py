# test_transformacion.py
import time
from transformacion import unificar_fuente_proyecto_beneficiario

def main():
    start = time.time()
    print("🧪 TEST: Transformación (Unificación N1+N2+N3)\n")

    try:
        unificar_fuente_proyecto_beneficiario.run()
    except Exception as e:
        print(f"[ERROR] Transformación: {e}")

    end = time.time()
    print(f"\n✅ Test completado en {end - start:.2f} segundos.")


if __name__ == "__main__":
    main()
