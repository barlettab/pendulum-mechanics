"""
Simular um sistema físico não linear simples que exibe movimento
oscilatório periódico, servindo como baseline determinístico previsível.

Características:
- Sistema não linear
- Movimento é periódico
- Baixa sensibilidade a pequenas perturbações
- Baixa complexidade dinâmica
"""

import numpy as np

def simulate_simple_pendulum(theta0, omega0, L=1, g=9.81, dt=0.02, steps=3000):

    theta = theta0
    omega = omega0

    theta_series = []

    for _ in range(steps):

        alpha = -(g / L) * np.sin(theta)

        omega += alpha * dt
        theta += omega * dt

        theta_series.append(theta)

    return np.array(theta_series)