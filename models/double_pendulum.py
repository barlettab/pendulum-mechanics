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

def _derivatives(state, m1, m2, L1, L2, g):
    theta1, omega1, theta2, omega2 = state

    delta = theta2 - theta1

    den1 = (m1 + m2)*L1 - m2*L1*np.cos(delta)**2
    den2 = (L2/L1)*den1

    domega1 = (
        m2*L1*omega1**2*np.sin(delta)*np.cos(delta)
        + m2*g*np.sin(theta2)*np.cos(delta)
        + m2*L2*omega2**2*np.sin(delta)
        - (m1+m2)*g*np.sin(theta1)
    ) / den1

    domega2 = (
        -m2*L2*omega2**2*np.sin(delta)*np.cos(delta)
        + (m1+m2)*g*np.sin(theta1)*np.cos(delta)
        - (m1+m2)*L1*omega1**2*np.sin(delta)
        - (m1+m2)*g*np.sin(theta2)
    ) / den2

    return np.array([omega1, domega1, omega2, domega2])

def _rk4_step(state, dt, m1, m2, L1, L2, g):

    k1 = _derivatives(state, m1, m2, L1, L2, g)
    k2 = _derivatives(state + 0.5 * dt * k1, m1, m2, L1, L2, g)
    k3 = _derivatives(state + 0.5 * dt * k2, m1, m2, L1, L2, g)
    k4 = _derivatives(state + dt * k3, m1, m2, L1, L2, g)

    return state + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)

def simulate_double_pendulum(
    theta1, theta2,
    omega1, omega2,
    L1=1, L2=1,
    m1=1, m2=1,
    g=9.81,
    dt=0.02,
    steps=3000,
    method="rk4"   # padrão recomendado
):

    theta1_series = []
    theta2_series = []

    state = np.array([theta1, omega1, theta2, omega2])

    for _ in range(steps):

        theta1_series.append(state[0])
        theta2_series.append(state[2])

        if method == "rk4":
            state = _rk4_step(state, dt, m1, m2, L1, L2, g)

        elif method == "euler":
            deriv = _derivatives(state, m1, m2, L1, L2, g)
            state = state + dt * deriv

        else:
            raise ValueError("method must be 'rk4' or 'euler'")

    return np.array(theta1_series), np.array(theta2_series)
