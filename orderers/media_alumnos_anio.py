# ==============================================================
# media_alumnos_anio.py
# Calcula la nota media de cada alumno por curso/año.
# El año se extrae del nombre de la asignatura:
#   - Busca el patrón número + letra(s) al final del nombre
#   - 1E = 1º ESO, 2E = 2º ESO, 3E = 3º ESO, 4E = 4º ESO
#   - 1B = 1º Bachillerato, 2B = 2º Bachillerato
#   - Variantes como EA, BA, SE, PM se agrupan igualmente
# Genera: media_alumnos_anio.csv
# ==============================================================

import re
import pandas as pd

# --- 1. Leer datos -----------------------------------------------------------
cal = pd.read_csv("cal_alumnos.csv", sep=";")

id_col = cal.columns[0]  # "exp"
asignaturas = cal.columns[1:]

# --- 2. Extraer curso de cada asignatura --------------------------------------
def extraer_curso(nombre):
    m = re.search(r"(\d)([A-Za-z]+)$", nombre)
    if not m:
        return None
    numero = m.group(1)
    letra = m.group(2)[0].upper()
    if letra == "E":
        return f"{numero}E"   # ESO
    if letra == "B":
        return f"{numero}B"   # Bachillerato
    if letra == "S":
        return f"{numero}E"   # SE -> ESO
    if letra == "P":
        return f"{numero}E"   # PM -> ESO
    return None

cursos = {asig: extraer_curso(asig) for asig in asignaturas}

# Resumen
from collections import Counter
conteo = Counter(v for v in cursos.values() if v is not None)
print("Cursos detectados:")
for k in sorted(conteo):
    print(f"  {k}: {conteo[k]} asignaturas")

# --- 3. Calcular media por alumno y curso ------------------------------------
niveles_orden = ["1E", "2E", "3E", "4E", "1B", "2B"]
cursos_presentes = [c for c in niveles_orden if c in conteo]

resultado = pd.DataFrame({"alumno": cal[id_col]})

for curso in cursos_presentes:
    cols = [asig for asig, c in cursos.items() if c == curso]
    notas = cal[cols]
    media = notas.mean(axis=1).round(2)
    # NA si el alumno no tiene ninguna nota en ese curso
    media[notas.isna().all(axis=1)] = pd.NA
    resultado[f"media_{curso}"] = media

# --- 4. Escribir CSV ----------------------------------------------------------
resultado.to_csv("media_alumnos_anio.csv", index=False)

print(f"\nArchivo 'media_alumnos_anio.csv' generado correctamente.")
print(f"  - {len(resultado)} alumnos")
print(f"  - Columnas: alumno, {', '.join(f'media_{c}' for c in cursos_presentes)}")
