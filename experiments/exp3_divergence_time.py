"""
O erro cresce exponencialmente?
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import numpy as np
import matplotlib.pyplot as plt

from models.double_pendulum import simulate_double_pendulum

# ==========================
# pasta do experimento
# ==========================
os.makedirs("data/exp3", exist_ok=True)

# ==========================
# simulações
# ==========================
A = simulate_double_pendulum(np.pi/2, np.pi/2, 0, 0)
B = simulate_double_pendulum(np.pi/2 + 0.0001, np.pi/2, 0, 0)

theta1_A, theta2_A = A
theta1_B, theta2_B = B

# ==========================
# erro (dataset principal)
# ==========================
error = np.abs(theta1_A - theta1_B)

# ==========================
# salvar dados
# ==========================
np.save("data/exp3/theta1_A.npy", theta1_A)
np.save("data/exp3/theta1_B.npy", theta1_B)

np.save("data/exp3/theta2_A.npy", theta2_A)
np.save("data/exp3/theta2_B.npy", theta2_B)

np.save("data/exp3/error.npy", error)

# ==========================
# plot
# ==========================
os.makedirs("plots/exp3", exist_ok=True)
plt.semilogy(error)
plt.title("Exponential error growth")
plt.ylabel("log |Δθ₁|")
plt.xlabel("time step")

plt.savefig("plots/exp3/error_growth.png", dpi=300, bbox_inches="tight")
plt.close()
