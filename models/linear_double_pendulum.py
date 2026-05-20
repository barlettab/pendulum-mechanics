import numpy as np

def _linear_derivatives(state, m1, m2, L1, L2, g):
    theta1, omega1, theta2, omega2 = state

    # --- SIMPLIFICAÇÃO LINEAR DOS DENOMINADORES ---
    # Como cos(delta) ~ 1 para ângulos pequenos, den1 simplifica para:
    # (m1 + m2) * L1 - m2 * L1 * 1 = m1 * L1
    den1 = m1 * L1
    den2 = (L2 / L1) * den1  # Simplifica para m1 * L2

    # --- SIMPLIFICAÇÃO LINEAR DOS NUMERADORES ---
    # 1. Zeramos os termos centrífugos/inerciais contendo omega^2 (não-lineares de ordem superior)
    # 2. Substituímos sin(theta) por theta e cos(delta) por 1
    
    domega1 = (
        0                                # m2 * L1 * omega1**2 * sin(delta) * cos(delta) -> 0
        + m2 * g * theta2 * 1            # sin(theta2) -> theta2, cos(delta) -> 1
        + 0                              # m2 * L2 * omega2**2 * sin(delta) -> 0
        - (m1 + m2) * g * theta1        # sin(theta1) -> theta1
    ) / den1

    domega2 = (
        0                                # -m2 * L2 * omega2**2 * sin(delta) * cos(delta) -> 0
        + (m1 + m2) * g * theta1 * 1     # sin(theta1) -> theta1, cos(delta) -> 1
        + 0                              # -(m1 + m2) * L1 * omega1**2 * sin(delta) -> 0
        - (m1 + m2) * g * theta2        # sin(theta2) -> theta2
    ) / den2

    return np.array([omega1, domega1, omega2, domega2])


def _linear_rk4_step(state, dt, m1, m2, L1, L2, g):
    k1 = _linear_derivatives(state, m1, m2, L1, L2, g)
    k2 = _linear_derivatives(state + 0.5 * dt * k1, m1, m2, L1, L2, g)
    k3 = _linear_derivatives(state + 0.5 * dt * k2, m1, m2, L1, L2, g)
    k4 = _linear_derivatives(state + dt * k3, m1, m2, L1, L2, g)

    return state + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)


def simulate_linear_double_pendulum(
    theta1, theta2,
    omega1, omega2,
    L1=1, L2=1,
    m1=1, m2=1,
    g=9.81,
    dt=0.005,
    steps=3000,
    method="rk4",
    return_omega=False
):
    """
    Simula o modelo linearizado (aproximação para pequenas oscilações)
    de um pêndulo duplo usando a mesma assinatura do modelo real.
    """
    theta1_series = []
    theta2_series = []
    omega1_series = []
    omega2_series = []

    state = np.array([theta1, omega1, theta2, omega2])

    for _ in range(steps):
        theta1_series.append(state[0])
        omega1_series.append(state[1])
        theta2_series.append(state[2])
        omega2_series.append(state[3])

        if method == "rk4":
            state = _linear_rk4_step(state, dt, m1, m2, L1, L2, g)

        elif method == "euler":
            deriv = _linear_derivatives(state, m1, m2, L1, L2, g)
            state = state + dt * deriv

        else:
            raise ValueError("method must be 'rk4' or 'euler'")

    if return_omega:
        return (
            np.array(theta1_series),
            np.array(theta2_series),
            np.array(omega1_series),
            np.array(omega2_series),
        )
    else:
        return (
            np.array(theta1_series),
            np.array(theta2_series)
        )