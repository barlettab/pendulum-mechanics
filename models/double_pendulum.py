"""
Simular um sistema físico acoplado de dois pêndulos, altamente sensível às condições iniciais,
utilizado como principal exemplo de caos determinístico.

Equações do sistema:
Sistema de equações diferenciais não lineares acopladas:
 - dependência entre θ₁ e θ₂
 - termos não lineares com seno e produtos de velocidades

Características
 - altamente não linear
 - forte acoplamento entre as variáveis
 - comportamento caótico
 - sensível a perturbações iniciais
"""

import numpy as np

def simulate_double_pendulum(
    theta1, theta2,
    omega1, omega2,
    L1=1, L2=1,
    m1=1, m2=1,
    g=9.81,
    dt=0.02,
    steps=3000
):

    theta1_series = []
    theta2_series = []

    for _ in range(steps):

        delta = theta2 - theta1

        den1 = (m1 + m2)*L1 - m2*L1*np.cos(delta)**2
        den2 = (L2/L1)*den1

        a1 = (
            m2*L1*omega1**2*np.sin(delta)*np.cos(delta)
            + m2*g*np.sin(theta2)*np.cos(delta)
            + m2*L2*omega2**2*np.sin(delta)
            - (m1+m2)*g*np.sin(theta1)
        ) / den1

        a2 = (
            -m2*L2*omega2**2*np.sin(delta)*np.cos(delta)
            + (m1+m2)*g*np.sin(theta1)*np.cos(delta)
            - (m1+m2)*L1*omega1**2*np.sin(delta)
            - (m1+m2)*g*np.sin(theta2)
        ) / den2

        omega1 += a1 * dt
        omega2 += a2 * dt

        theta1 += omega1 * dt
        theta2 += omega2 * dt

        theta1_series.append(theta1)
        theta2_series.append(theta2)

    return np.array(theta1_series), np.array(theta2_series)