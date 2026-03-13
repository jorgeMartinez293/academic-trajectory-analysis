import pandas as pd

df = pd.read_csv('calificaciones.csv', encoding='utf-8', delimiter=';')

new_df = df.pivot_table(index='exp', 
                          columns='materia', 
                          values='valor', 
                          aggfunc='last'
                        )
new_df.reset_index()
new_df.to_csv('cal_alumnos.csv', encoding='utf-8', sep=';')