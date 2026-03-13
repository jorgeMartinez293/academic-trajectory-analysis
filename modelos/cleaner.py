import csv

files_novatos = ['Calificaciones1617.csv', 'Calificaciones1718.csv', 'Calificaciones1819.csv', 'Calificaciones1920.csv', 'Calificaciones2021.csv']
files = ['Calificaciones1617.csv', 'Calificaciones1718.csv', 'Calificaciones1819.csv', 'Calificaciones1920.csv', 'Calificaciones2021.csv', 'Calificaciones2122.csv', 'Calificaciones2223.csv', 'Calificaciones2324.csv', 'Calificaciones2425.csv']

novatos = set()
mega_df = []

for file in files:
    with open('./calificaciones/' + file, mode='r', encoding='latin1') as f:
        reader = csv.DictReader(f, delimiter=';')

        for row in reader:
            if row['desmat'] == 'Matemï¿½ticas' and row['nivel'] == '1' and 'Educaciï¿½n Secundaria Obligatoria (LOMCE)' in row['descripcion'] and file in files_novatos:
                novatos.add(row['exp'])
            mega_df.append(row)
            

print(f'novatos encontrados: {len(novatos)}')

cabecera = ['mat1ESO', 'mat2ESO', 'mat3ESO', 'mat4ESO', 'mat1BAC', 'mat2BAC']
#alumnos = [i for i in range(696)]
mat1ESO = []
mat2ESO = []
mat3ESO = []
mat4ESO = []
mat1BAC = []
mat2BAC = []

for n in novatos:
    nota1, nota2, nota3, nota4, nota1b, nota2b = None, None, None, None, None, None
    for row in mega_df:
        if row['exp'] == n:
            if 'Matemï¿½ticas' in row['desmat']:
                if 'Educaciï¿½n Secundaria Obligatoria (LOMCE)' in row['descripcion']:
                    if row['nivel'] == '1':
                            nota1 = row['valor']
                    elif row['nivel'] == '2':
                            nota2 = row['valor']
                    elif row['nivel'] == '3':
                            nota3 = row['valor']
                    elif row['nivel'] == '4':
                            nota4 = row['valor']
                elif 'Bachillerato' in row['descripcion']:
                    if row['nivel'] == '1':
                            nota1b = row['valor']
                    elif row['nivel'] == '2':
                            nota2b = row['valor']

    mat1ESO.append(nota1)
    mat2ESO.append(nota2)
    mat3ESO.append(nota3)
    mat4ESO.append(nota4)
    mat1BAC.append(nota1b)
    mat2BAC.append(nota2b)

with open('clean.csv', mode='w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, delimiter=';')

    writer.writerow(cabecera)

    for row in zip(mat1ESO, mat2ESO, mat3ESO, mat4ESO, mat1BAC, mat2BAC):
        writer.writerow(row)