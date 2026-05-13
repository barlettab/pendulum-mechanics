"""
Media separação entre duas trajetórias quase iguais
(Butterfly effect)
"""

import numpy as np

def divergence(x1, y1, x2, y2):

    return np.sqrt((x1 - x2)**2 + (y1 - y2)**2)