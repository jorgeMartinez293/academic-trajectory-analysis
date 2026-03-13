# ==============================================================
# media_alumnos_filtrado.py
# 1. Lee los 4 primeros ficheros de calificaciones (16/17 a 19/20)
# 2. Selecciona solo alumnos que cursan MAT1E
# 3. Calcula la nota media por curso/año para esos alumnos
# 4. Renumera los expedientes como 0, 1, 2, ...
# Genera: media_alumnos_filtrado.csv
# ==============================================================

import re
import pandas as pd
from pathlib import Path

# --- 1. Identificar alumnos con MAT1E en los 4 primeros ficheros --------------
carpeta = Path("calificaciones")
todos_ficheros = sorted(carpeta.glob("Calificaciones*.csv"))
ficheros_inicio = todos_ficheros[:4]

print("Ficheros para identificar alumnos (MAT1E):")
for f in ficheros_inicio:
    print(f"  - {f.name}")

dfs_inicio = []
for f in ficheros_inicio:
    df = pd.read_csv(f, sep=";", encoding="latin-1")
    dfs_inicio.append(df)

cal_inicio = pd.concat(dfs_inicio, ignore_index=True)
exps_mat1e = cal_inicio.loc[cal_inicio["materia"] == "MAT1E", "exp"].unique()
print(f"\nAlumnos con MAT1E: {len(exps_mat1e)}")

# --- 2. Leer TODOS los ficheros y filtrar solo esos alumnos -------------------
print("\nFicheros para calcular medias:")
dfs_todos = []
for f in todos_ficheros:
    df = pd.read_csv(f, sep=";", encoding="latin-1")
    dfs_todos.append(df)
    print(f"  - {f.name}")

cal = pd.concat(dfs_todos, ignore_index=True)
cal["valor"] = pd.to_numeric(cal["valor"], errors="coerce")

# --- 3. Filtrar solo alumnos con MAT1E ----------------------------------------
cal = cal[cal["exp"].isin(exps_mat1e)]


# --- 3. Extraer curso de cada asignatura --------------------------------------
def extraer_curso(nombre):
    m = re.search(r"(\d)([A-Za-z]+)$", str(nombre))
    if not m:
        return None
    numero = m.group(1)
    letra = m.group(2)[0].upper()
    if letra == "E":
        return f"{numero}E"
    if letra == "B":
        return f"{numero}B"
    if letra == "S":
        return f"{numero}E"
    if letra == "P":
        return f"{numero}E"
    return None

cal["curso"] = cal["materia"].apply(extraer_curso)
cal = cal.dropna(subset=["curso"])

# --- 4. Calcular media por alumno y curso ------------------------------------
niveles_orden = ["1E", "2E", "3E", "4E", "1B", "2B"]

media = (
    cal.groupby(["exp", "curso"])["valor"]
    .mean()
    .round(2)
    .unstack("curso")
)

# Reordenar columnas según niveles
cols_presentes = [c for c in niveles_orden if c in media.columns]
media = media[cols_presentes]
media.columns = [f"media_{c}" for c in cols_presentes]

# --- 5. Renumerar expedientes como 0, 1, 2, ... ------------------------------
media = media.reset_index(drop=True)
media.index.name = "alumno"
media = media.reset_index()

# --- 6. Escribir CSV ----------------------------------------------------------
media.to_csv("media_alumnos_filtrado.csv", index=False)

print(f"\nArchivo 'media_alumnos_filtrado.csv' generado correctamente.")
print(f"  - {len(media)} alumnos")
print(f"  - Columnas: {', '.join(media.columns)}")
