# ==============================================================
# nota_media_docentes.py
# Calcula la nota media de cada docente:
#   - Por cada asignatura que imparte
#   - Media general (todas las asignaturas)
# Genera: nota_media_docentes.csv
# ==============================================================

import pandas as pd

# --- 1. Leer datos -----------------------------------------------------------
cal = pd.read_csv("calificaciones.csv", sep=";")

# --- 2. Media por docente y asignatura ----------------------------------------
media_asig = (
    cal.groupby(["docente", "materia"])["valor"]
    .mean()
    .round(2)
    .reset_index()
    .rename(columns={"valor": "nota_media"})
)

# --- 3. Media general por docente ---------------------------------------------
media_gral = (
    cal.groupby("docente")["valor"]
    .mean()
    .round(2)
    .reset_index()
    .rename(columns={"valor": "nota_media"})
)
media_gral["materia"] = "GENERAL"

# --- 4. Combinar y ordenar ----------------------------------------------------
resultado = (
    pd.concat([media_asig, media_gral], ignore_index=True)
    .sort_values(["docente", "materia"])
    [["docente", "materia", "nota_media"]]
)

# --- 5. Escribir CSV ----------------------------------------------------------
resultado.to_csv("nota_media_docentes.csv", index=False)

print("Archivo 'nota_media_docentes.csv' generado correctamente.")
print(f"  - {resultado['docente'].nunique()} docentes")
print(f"  - {len(resultado)} filas (asignaturas + medias generales)")
