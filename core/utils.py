"""
Funções auxiliares
"""

import numpy as np

def align_series(a, b):
    """
    Alinha duas séries temporais para comparação
    """
    min_len = min(len(a), len(b))
    return np.array(a[:min_len]), np.array(b[:min_len])


def normalize(series):
    series = np.array(series)
    return (series - np.mean(series)) / (np.std(series) + 1e-12)