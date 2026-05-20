"""
Utilizar o Theil's U statistic para medir a qualidade de previsão
comparando a série real com a série prevista.

Implementação adotada (Theil U2 / relative RMSE):
U = RMSE(modelo) / RMSE(naive persistente)

* U = 0 : previsão perfeita
* U < 1 : modelo melhor que o ingênuo
* U = 1 : modelo equivalente ao ingênuo
* U > 1 : pior que baseline ingênuo
"""

import numpy as np


def theils_u(y_true, y_pred, eps=1e-12):
    """Calcula Theil's U2 com baseline ingênuo de persistência.

    Args:
        y_true: série real.
        y_pred: série prevista.
        eps: termo de estabilidade numérica para evitar divisão por zero.
    """

    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)

    n = min(len(y_true), len(y_pred))
    if n < 2:
        raise ValueError("theils_u requires at least 2 points in each series")

    y_true = y_true[:n]
    y_pred = y_pred[:n]

    mse_model = np.mean((y_true - y_pred) ** 2)
    mse_naive = np.mean((y_true[1:] - y_true[:-1]) ** 2)

    return np.sqrt(mse_model) / (np.sqrt(mse_naive) + eps)
