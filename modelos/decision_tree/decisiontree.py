######################
# Importar librerías #
######################

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.tree import plot_tree
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt
import numpy as np

#################
# Cargar el csv #
#################

df_entero = pd.read_csv('../clean.csv', sep=';')
columnas_criticas = df_entero.columns[:-1]
df = df_entero.dropna(subset=columnas_criticas)

#####################
# Dividir los datos #
#####################

seed = 12
X_train, X_test, y_train, y_test = train_test_split(
                                        df.drop(columns = ["mat1BAC", "mat2BAC", "mat1ESO"]), # Aquí especificas que columnas no quieres usar
                                        df['mat1BAC'],
                                        random_state = seed
                                    )
####################################
# Obtener hipermparámetros óptimos #
####################################

param_grid = {'ccp_alpha':np.linspace(0, 20)}

grid = GridSearchCV(
        estimator = DecisionTreeRegressor(
                            max_depth         = None,
                            min_samples_split = 2,
                            min_samples_leaf  = 1,
                            random_state      = seed
                       ),
        param_grid = param_grid,
        cv         = 10,
        refit      = True,
        return_train_score = True
      )

grid.fit(X_train, y_train)

################
# Crear modelo #
################

d_tree = grid.best_estimator_

fig, ax = plt.subplots(figsize=(12, 5))

plot = plot_tree(
            decision_tree = d_tree,
            feature_names = df.drop(columns = 'mat1BAC').columns,
            class_names   = None,
            filled        = True,
            impurity      = False,
            fontsize      = 10,
            precision     = 2,
            ax            = ax
       )
plt.show()

#####################################
# Comprobar precisión de resultados #
#####################################

import matplotlib.pyplot as plt

y_pred = d_tree.predict(X_test)

plt.scatter(y_test, y_pred, color='blue', alpha=0.5)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
plt.xlabel('Nota Real')
plt.ylabel('Predicción')
plt.show()

mae_dt = mean_absolute_error(
        y_true  = y_test,
        y_pred  = y_pred
       )
print(f"El error (mae) de test es: {mae_dt:.2f}")