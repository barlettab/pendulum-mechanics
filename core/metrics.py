"""
Utilizar o Theil's U statistic para medir a qualidade de previsão
comparando a série real com a série prevista.

* U = 0 : previsão perfeita
* U < 1 : modelo melhor que o ingênuo
* U = 1 : modelo ingênuo
* U > 1 : pior que baseline ingênuo
"""

import numpy as np

def theils_u(y_true, y_pred):

    y_true = np.array(y_true)
    y_pred = np.array(y_pred)

    mse_model = np.mean((y_true - y_pred)**2)
    mse_naive = np.mean((y_true[1:] - y_true[:-1])**2)

    return np.sqrt(mse_model) / np.sqrt(mse_naive)