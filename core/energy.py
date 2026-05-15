import numpy as np

# ==========================
# PÊNDULO SIMPLES
# ==========================

def simple_pendulum_energy(theta, omega, m=1.0, L=1.0, g=9.81):
    """
    Energia total do pêndulo simples:
    E = K + U
    """

    kinetic = 0.5 * m * (L * omega)**2
    potential = m * g * L * (1 - np.cos(theta))

    return kinetic + potential


# ==========================
# PÊNDULO DUPLO
# ==========================

def double_pendulum_energy(theta1, omega1, theta2, omega2,
                            m1=1.0, m2=1.0,
                            L1=1.0, L2=1.0,
                            g=9.81):
    """
    Energia total do pêndulo duplo (forma padrão simplificada)
    """

    # velocidades lineares
    v1_sq = (L1 * omega1)**2

    v2_sq = (
        (L1 * omega1)**2 +
        (L2 * omega2)**2 +
        2 * L1 * L2 * omega1 * omega2 * np.cos(theta1 - theta2)
    )

    # energias cinéticas
    kinetic = 0.5 * m1 * v1_sq + 0.5 * m2 * v2_sq

    # energias potenciais
    y1 = -L1 * np.cos(theta1)
    y2 = y1 - L2 * np.cos(theta2)

    potential = m1 * g * (y1 + L1) + m2 * g * (y2 + L1 + L2)

    return kinetic + potential

def energy_drift(E):

    E0 = E[0]

    drift = np.max(np.abs(E - E0)) / np.abs(E0)

    return drift
