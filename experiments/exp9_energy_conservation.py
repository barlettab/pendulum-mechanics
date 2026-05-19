import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import numpy as np
import matplotlib.pyplot as plt

from models.simple_pendulum import simulate_simple_pendulum
from models.double_pendulum import simulate_double_pendulum
from core.energy import simple_pendulum_energy, double_pendulum_energy, energy_drift


# ==========================
# SETUP
# ==========================
os.makedirs("data/exp7", exist_ok=True)
os.makedirs("plots/exp7", exist_ok=True)

steps = 3000
dt = 0.005
time = np.arange(steps) * dt


# ==========================
# SIMULAÇÃO — PÊNDULO SIMPLES
# ==========================
theta_simple, omega_simple = simulate_simple_pendulum(
    theta0=0.8,
    omega0=0,
    steps=steps,
    dt=dt,
    return_omega=True
)


# ==========================
# SIMULAÇÃO — PÊNDULO DUPLO
# ==========================
theta1, theta2, omega1, omega2 = simulate_double_pendulum(
    theta1=np.pi/2,
    theta2=np.pi/2,
    omega1=0,
    omega2=0,
    steps=steps,
    dt=dt,
    return_omega=True
)


# ==========================
# ENERGIA — PÊNDULO SIMPLES
# ==========================
E_simple = np.array([
    simple_pendulum_energy(theta_simple[i], omega_simple[i])
    for i in range(len(theta_simple))
])


# ==========================
# ENERGIA — PÊNDULO DUPLO
# ==========================
E_double = np.array([
    double_pendulum_energy(
        theta1[i], omega1[i],
        theta2[i], omega2[i]
    )
    for i in range(len(theta1))
])


# ==========================
# ENERGY DRIFT
# ==========================
drift_simple = energy_drift(E_simple)
drift_double = energy_drift(E_double)


# ==========================
# NORMALIZAÇÃO
# ==========================
E_simple_norm = E_simple / E_simple[0]
E_double_norm = E_double / E_double[0]


# ==========================
# SALVAR DADOS
# ==========================
np.save("data/exp7/E_simple.npy", E_simple)
np.save("data/exp7/E_double.npy", E_double)


# ==========================
# FIGURA CIENTÍFICA
# ==========================
fig, axs = plt.subplots(1, 2, figsize=(10,4))


# -------- A) PÊNDULO SIMPLES
axs[0].plot(time, E_simple_norm)
axs[0].axhline(1, linestyle="--", color="black", linewidth=1)

axs[0].set_title("A) Pêndulo Simples")
axs[0].set_xlabel("tempo (s)")
axs[0].set_ylabel("energia normalizada")

axs[0].grid(alpha=0.3)


# -------- B) PÊNDULO DUPLO
axs[1].plot(time, E_double_norm)
axs[1].axhline(1, linestyle="--", color="black", linewidth=1)

axs[1].set_title("B) Pêndulo Duplo")
axs[1].set_xlabel("tempo (s)")
axs[1].set_ylabel("energia normalizada")

axs[1].grid(alpha=0.3)


plt.tight_layout()

plt.savefig(
    "plots/exp7/energy_conservation.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ==========================
# RESULTADOS
# ==========================
print("Energy Drift Results")
print("--------------------")

print(f"Simple Pendulum: {drift_simple:.6e}")
print(f"Double Pendulum: {drift_double:.6e}")
