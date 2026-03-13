######################
# Importar librerias #
######################

import pandas as pd # Para tratar el csv
from sklearn.model_selection import train_test_split # Para dividir los datos
from sklearn.linear_model import LinearRegression # El modelo de regresión lineal
import matplotlib.pyplot as plt # Para mostrar las gráficas
from sklearn.metrics import mean_absolute_error # Para calcular el error absoluto medio

#################
# Cargar el csv #
#################

df_entero = pd.read_csv('../clean.csv', sep=';')
columnas_criticas = df_entero.columns[:-1]
df = df_entero.dropna(subset=columnas_criticas)
df = df.reset_index(drop=True)

#####################
# Dividir los datos #
#####################

seed = 12
X_train, X_test, y_train, y_test = train_test_split(
                                        df.drop(columns = ["mat1BAC", "mat2BAC", "mat1ESO"]), # Aquí especificas que columnas no quieres usar
                                        df['mat1BAC'],
                                        random_state = seed
                                    )

######################
# Entrenar el modelo #
######################

regresion = LinearRegression() # Definir el modelo
regresion.fit(X_train, y_train) # Entrenarlo

print(f'coeficientes: {regresion.coef_}') # Enseñar los coeficientes
print(f'offset: {regresion.intercept_}') # Esnseñar el intercepto
y_pred = regresion.predict(X_test) # Calculamos las predicciones

# Calculamos el error absoluto medio
mae_dt = mean_absolute_error(
        y_true  = y_test,
        y_pred  = y_pred
       )

print(f"El error (mae) de test es: {mae_dt:.2f}") # Mostramos el mae

# Representación gráfica
plt.scatter(y_test, y_pred, color='blue', alpha=0.5)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2) # rango eje x, rango eje y, y formato de la recta
plt.xlabel('Nota Real')
plt.ylabel('Predicción')
plt.show()