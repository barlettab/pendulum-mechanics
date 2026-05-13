import numpy as np

# ================================
# MODELO 1 — PÊNDULO SIMPLES
# ================================

def simulate_simple_pendulum(theta0, omega0, L=1, g=9.81, dt=0.02, steps=3000):

    theta = theta0
    omega = omega0

    theta_series = []

    for _ in range(steps):

        alpha = -(g/L) * np.sin(theta)

        omega += alpha * dt
        theta += omega * dt

        theta_series.append(theta)

    return np.array(theta_series)


# ================================
# MODELO 2 — PÊNDULO DUPLO
# ================================

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

        den1 = (2*m1 + m2 - m2*np.cos(2*theta1 - 2*theta2))
        den2 = den1

        a1 = (
            -g*(2*m1 + m2)*np.sin(theta1)
            - m2*g*np.sin(theta1 - 2*theta2)
            - 2*np.sin(delta)*m2*(omega2**2*L2 + omega1**2*L1*np.cos(delta))
        ) / (L1 * den1)

        a2 = (
            2*np.sin(delta)*(
                omega1**2*L1*(m1+m2)
                + g*(m1+m2)*np.cos(theta1)
                + omega2**2*L2*m2*np.cos(delta)
            )
        ) / (L2 * den2)

        omega1 += a1 * dt
        omega2 += a2 * dt

        theta1 += omega1 * dt
        theta2 += omega2 * dt

        theta1_series.append(theta1)
        theta2_series.append(theta2)

    return np.array(theta1_series), np.array(theta2_series)

# ================================
# MODELO 3 — PÊNDULO LINEARIZADO
# ================================
def simulate_linear_pendulum(theta0, omega0, L=1, g=9.81, dt=0.02, steps=3000):

    theta = theta0
    omega = omega0

    theta_series = []

    for _ in range(steps):

        alpha = -(g/L) * theta   # aproximação linear

        omega += alpha * dt
        theta += omega * dt

        theta_series.append(theta)

    return np.array(theta_series)


# ================================
# TESTE RÁPIDO
# ================================

if __name__ == "__main__":

    # pêndulo simples
    simple = simulate_simple_pendulum(
        theta0=0.8,
        omega0=0
    )

    # pêndulo duplo
    theta1, theta2 = simulate_double_pendulum(
        theta1=1.0,
        theta2=1.0,
        omega1=0,
        omega2=0
    )

    print("Simulação concluída")