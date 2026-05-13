import numpy as np
import matplotlib.pyplot as plt

from pendulum_models import (
    simulate_simple_pendulum,
    simulate_linear_pendulum
)

from metrics import theils_u


# condições iniciais
theta0 = 1.2
omega0 = 0

# simulações
theta_real = simulate_simple_pendulum(theta0, omega0)
theta_pred = simulate_linear_pendulum(theta0, omega0)


# calcular Theil's U ao longo do tempo
U_series = []

for t in range(20, len(theta_real)):

    U = theils_u(
        theta_real[:t],
        theta_pred[:t]
    )

    U_series.append(U)


# gráfico
plt.figure(figsize=(10,5))

plt.plot(U_series)

plt.title("Prediction Error Growth (Theil's U)")
plt.xlabel("time step")
plt.ylabel("Theil's U")

plt.show()