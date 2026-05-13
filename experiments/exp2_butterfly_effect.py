"""
Pequenas diferenças iniciais geram grandes diferenças?
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import numpy as np
import matplotlib.pyplot as plt

from models.double_pendulum import simulate_double_pendulum
from core.divergence import divergence

# ==========================
# criar pasta de dados
# ==========================
os.makedirs("data/exp2", exist_ok=True)


# ==========================
# simulações
# ==========================
A = simulate_double_pendulum(np.pi/2, np.pi/2, 0, 0)
B = simulate_double_pendulum(np.pi/2 + 0.001, np.pi/2, 0, 0)

theta1_A, theta2_A = A
theta1_B, theta2_B = B

# ==========================
# salvar dados (AQUI!)
# ==========================
np.save("data/exp2/theta1_A.npy", theta1_A)
np.save("data/exp2/theta2_A.npy", theta2_A)

np.save("data/exp2/theta1_B.npy", theta1_B)
np.save("data/exp2/theta2_B.npy", theta2_B)

# ==========================
# análise
# ==========================
dist = divergence(theta1_A, theta2_A, theta1_B, theta2_B)

# ==========================
# plot
# ==========================
os.makedirs("plots/exp2", exist_ok=True)
plt.plot(dist)
plt.title("Butterfly Effect - trajectory divergence")
plt.show()

plt.savefig("plots/exp2/butterfly_effect.png", dpi=300, bbox_inches="tight")
plt.close()