import pandas as pd
import json

def desc(mat, file_map='mapeos.json'):
    with open(file_map, 'r', encoding='utf-8') as f:
        descripciones = json.load(f)
    return descripciones[mat]

df = pd.read_csv('cal_alumnos.csv', encoding='utf-8', delimiter=';')

col_mat = ['MAA3E', 'MAA4E', 'MAB3E', 'MAB4E', 'MAT1B', 'MAT1BA', 'MAT1E', 'MAT1EA', 'MAT2B', 'MAT2BA', 'MAT2E', 'MAT2EA', 'MAT3EA', 'MCS1B', 'MCS1BA', 'MCS2B', 'MCS2BA']
df = df[col_mat]
df['MAT1B'] = df['MAT1B'].fillna(df['MAT1BA'])
df['MAT1E'] = df['MAT1E'].fillna(df['MAT1EA'])
df['MAT2B'] = df['MAT2B'].fillna(df['MAT2BA'])
df['MAT2E'] = df['MAT2E'].fillna(df['MAT2EA'])
df['MAT3E'] = df['MAA3E'].fillna(df['MAB3E'])
df['MAT3E'] = df['MAA3E'].fillna(df['MAT3EA'])
df['MAT4E'] = df['MAA4E'].fillna(df['MAB4E'])
#df['MAB2E'] = df['MAT2E'].fillna(df['MAT2EA'])

lomce = ['MAT2BA', 'MAT2EA', 'MAB3E', 'MAA3E', 'MAT1BA', 'MAT1EA', 'MAT3EA', 'MAA4E', 'MAB4E']
df = df.drop(columns=lomce)

print(df.head(5))
print(desc('MAA3E'))
print(desc('MAB3E'))