######################
# Importar librerías #
######################

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import RandomizedSearchCV
import numpy as np
from scipy.stats import randint
import matplotlib.pyplot as plt

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

#########################################
# Encontrar los mejores hiperparámetros #
#########################################

param_distributions = {
    'n_estimators': [1, 500],
    'max_depth': randint(1, 50),
    'min_samples_split': randint(2, 20),
    'min_samples_leaf': randint(1, 10),
    'max_features': ['sqrt', 'log2']
}

rf = RandomForestRegressor(random_state=seed)

random_search = RandomizedSearchCV(
    estimator=rf,
    param_distributions=param_distributions,
    cv=5,
    random_state=seed,
    n_jobs=-1,
    scoring='neg_mean_squared_error'
)

################################
# Entrenar y evaluar el modelo #
################################

random_search.fit(X_train, y_train)

y_pred = random_search.predict(X_test)

plt.scatter(y_test, y_pred, color='blue', alpha=0.5)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
plt.xlabel('Nota Real')
plt.ylabel('Predicción')
plt.show()

mae_rf = mean_absolute_error(
        y_true  = y_test,
        y_pred  = y_pred
       )
print(f"El error (mae) de test es: {mae_rf:.2f}")