"""
Medir a desordem estatística das trajetórias

Interpretação:
* Baixa entropia = movimento regular
* Alta entropia = caos
"""

import numpy as np

def entropy(series, bins=50):

    hist, _ = np.histogram(series, bins=bins, density=True)

    hist = hist + 1e-12  # evita log(0)

    p = hist / np.sum(hist)

    return -np.sum(p * np.log(p))