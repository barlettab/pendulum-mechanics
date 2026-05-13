import numpy as np


def mse(y_true, y_pred):
    """
    Mean Squared Error
    """
    return np.mean((y_true - y_pred) ** 2)


def rmse(y_true, y_pred):
    """
    Root Mean Squared Error
    """
    return np.sqrt(mse(y_true, y_pred))


def mae(y_true, y_pred):
    """
    Mean Absolute Error
    """
    return np.mean(np.abs(y_true - y_pred))


def theils_u(y_true, y_pred):
    """
    Theil's U statistic
    Mede qualidade relativa da previsão
    """

    numerator = np.sqrt(np.mean((y_true - y_pred) ** 2))

    denominator = (
        np.sqrt(np.mean(y_true ** 2)) +
        np.sqrt(np.mean(y_pred ** 2))
    )

    return numerator / denominator


def entropy(series, bins=50):

    hist, _ = np.histogram(series, bins=bins, density=True)

    hist = hist + 1e-12  # evitar log(0)

    p = hist / np.sum(hist)

    H = -np.sum(p * np.log(p))

    return H