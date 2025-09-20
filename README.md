SED/
│── main.py                      # Script principal de orquestación (extracción)
│── main2.py                     # Script alterno de test de transformaciones
│
├── extraccion/
│   ├── nivel1_fuentes/
│   │   ├── extraccion_fuente_estrategias.py
│   │   ├── extraccion_fuente_poai_2024.py
│   │   ├── extraccion_fuente_poai_2025.py
│   │   ├── extraccion_fuente_regalias.py
│   │   └── __init__.py
│   │
│   ├── nivel2_proyectos/
│   │   ├── extraccion_proyectos_estrategia.py
│   │   ├── extraccion_proyectos_poai_2024.py
│   │   ├── extraccion_proyectos_poai_2025.py
│   │   ├── extraccion_proyectos_regalias.py
│   │   └── __init__.py
│   │
│   ├── nivel3_beneficiarios/
│   │   ├── extraccion_beneficiarios_estrategia.py
│   │   ├── extraccion_beneficiarios_poai_2024.py (si aplica)
│   │   ├── extraccion_beneficiarios_poai_2025.py (si aplica)
│   │   ├── extraccion_beneficiarios_regalias.py (si aplica)
│   │   └── __init__.py
│   │
│   ├── outputs/                  # Resultados de extracción por cada nivel
│   │   ├── Registros_Fuente_*.xlsx
│   │   ├── Registro_Proyectos_Actividades_*.xlsx
│   │   └── Registro_Beneficiarios_*.xlsx
│   │
│   └── utils/
│       ├── excel_utils.py
│       ├── export_utils.py
│       ├── proyectos_utils.py
│       ├── proyectos_helpers.py
│       └── __init__.py
│
├── transformacion/
│   ├── transformar_poai_2024.py
│   ├── transformar_poai_2025.py
│   ├── transformar_estrategias.py
│   ├── transformar_regalias.py
│   │
│   ├── utils/
│   │   ├── transform_utils.py   # Última versión: genera 3 outputs separados
│   │   └── __init__.py
│   │
│   ├── staging/                  # Resultados de la transformación
│   │   ├── fact_fuente_poai_2024.xlsx
│   │   ├── fact_proyectos_poai_2024.xlsx
│   │   ├── fact_beneficiarios_poai_2024.xlsx
│   │   ├── fact_fuente_poai_2025.xlsx
│   │   ├── fact_proyectos_poai_2025.xlsx
│   │   ├── fact_beneficiarios_poai_2025.xlsx
│   │   ├── fact_fuente_estrategias.xlsx
│   │   ├── fact_proyectos_estrategias.xlsx
│   │   ├── fact_beneficiarios_estrategias.xlsx
│   │   ├── fact_fuente_regalias.xlsx
│   │   ├── fact_proyectos_regalias.xlsx
│   │   ├── fact_beneficiarios_regalias.xlsx
│   │   └── resumen_transformacion.xlsx   # Resumen de test
│
├── relacion/
│   └── Relación entre fuentes.xlsx   # Archivo maestro con columnas: Nombre Proyecto, FUENTES, PROYECTOS, BENEFICIARIOS
│
├── test_transformacion.py        # Test unificado con conteos por nivel
│
└── .venv/                        # Entorno virtual




