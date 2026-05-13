import numpy as np
import matplotlib.pyplot as plt

from pendulum_models import (
    simulate_simple_pendulum,
    simulate_linear_pendulum
)

from metrics import theils_u


# =============================
# EXPERIMENTO 1
# Pêndulo simples
# =============================

theta_real = simulate_simple_pendulum(
    theta0=0.8,
    omega0=0
)

theta_pred = simulate_linear_pendulum(
    theta0=0.8,
    omega0=0
)

score = theils_u(theta_real, theta_pred)

print("Theil's U (simple pendulum):", score)


plt.figure(figsize=(10,4))

plt.plot(theta_real, label="Real system (sin θ)")
plt.plot(theta_pred, label="Linear model (θ)", alpha=0.7)

plt.legend()
plt.title("Real Pendulum vs Linear Approximation")
plt.xlabel("time step")
plt.ylabel("θ")

plt.show()