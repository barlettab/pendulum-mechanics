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

def simulate_simple_pendulum(theta0, omega0, steps=3000, dt=0.005, return_omega=False):

    g = 9.81
    L = 1

    theta = np.zeros(steps)
    omega = np.zeros(steps)

    theta[0] = theta0
    omega[0] = omega0

    for i in range(steps - 1):

        omega[i+1] = omega[i] - (g/L) * np.sin(theta[i]) * dt
        theta[i+1] = theta[i] + omega[i+1] * dt

    if return_omega:
        return theta, omega
    else:
        return theta
