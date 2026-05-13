"""
Aproximar o pêndulo simples usando a hipótese de pequenos ângulos: sin(theta) ≈ theta

Características
- Sistema linear
- Solução analítica conhecida
- Não captura comportamento real para grandes amplitudes

Objetivo - servir como modelo ingênuo (naive) e base de cálculo para o Theil's U

"""

import numpy as np

def simulate_linear_pendulum(theta0, omega0, L=1, g=9.81, dt=0.02, steps=3000):

    theta = theta0
    omega = omega0

    theta_series = []

    for _ in range(steps):

        alpha = -(g / L) * theta  # linearização

        omega += alpha * dt
        theta += omega * dt

        theta_series.append(theta)

    return np.array(theta_series)