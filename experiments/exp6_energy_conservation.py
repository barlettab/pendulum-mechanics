import os
import numpy as np
import matplotlib.pyplot as plt

from models.simple_pendulum import simulate_simple_pendulum
from models.double_pendulum import simulate_double_pendulum
from core.energy import simple_pendulum_energy, double_pendulum_energy


# ==========================
# setup
# ==========================
os.makedirs("data/exp6", exist_ok=True)
os.makedirs("plots/exp6", exist_ok=True)

steps = 3000


# ==========================
# SIMULAÇÕES
# ==========================
theta_simple, omega_simple = simulate_simple_pendulum(
    theta0=0.8,
    omega0=0,
    return_omega=True
)

theta1, theta2, omega1, omega2 = simulate_double_pendulum(
    theta1=np.pi/2,
    theta2=np.pi/2,
    omega1=0,
    omega2=0,
    return_omega=True
)


# ==========================
# ENERGIA - PÊNDULO SIMPLES
# ==========================
E_simple = np.array([
    simple_pendulum_energy(theta_simple[i], omega_simple[i])
    for i in range(len(theta_simple))
])


# ==========================
# ENERGIA - PÊNDULO DUPLO
# ==========================
E_double = np.array([
    double_pendulum_energy(
        theta1[i], omega1[i],
        theta2[i], omega2[i]
    )
    for i in range(len(theta1))
])


# ==========================
# NORMALIZAÇÃO (opcional)
# ==========================
E_simple_norm = E_simple / E_simple[0]
E_double_norm = E_double / E_double[0]


# ==========================
# SALVAR DADOS
# ==========================
np.save("data/exp6/E_simple.npy", E_simple)
np.save("data/exp6/E_double.npy", E_double)


# ==========================
# PLOT
# ==========================
plt.figure(figsize=(10,4))

plt.plot(E_simple_norm, label="Simple Pendulum")
plt.plot(E_double_norm, label="Double Pendulum")

plt.title("Energy Conservation Over Time")
plt.xlabel("time step")
plt.ylabel("normalized energy")
plt.legend()

plt.savefig("plots/exp6/energy_conservation.png", dpi=300, bbox_inches="tight")
plt.close()


# ==========================
# MÉTRICA SIMPLES DE DRIFT
# ==========================
drift_simple = np.std(E_simple_norm - 1)
drift_double = np.std(E_double_norm - 1)

print("Energy drift (simple):", drift_simple)
print("Energy drift (double):", drift_double)
