"""
O modelo linear consegue prever um sistema não linear (pêndulo simples)?
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import numpy as np
import matplotlib.pyplot as plt

from models.simple_pendulum import simulate_simple_pendulum
from models.linear_pendulum import simulate_linear_pendulum
from core.metrics import theils_u

# ==========================
# pasta de dados
# ==========================
os.makedirs("data/exp1", exist_ok=True)


# ==========================
# simulações
# ==========================
theta_real = simulate_simple_pendulum(0.8, 0)
theta_pred = simulate_linear_pendulum(0.8, 0)

# ==========================
# métrica
# ==========================
U = theils_u(theta_real, theta_pred)

print("Theil's U:", U)

# ==========================
# salvar dados 
# ==========================
np.save("data/exp1/theta_real.npy", theta_real)
np.save("data/exp1/theta_pred.npy", theta_pred)
np.save("data/exp1/theils_u.npy", np.array([U]))

# ==========================
# plot
# ==========================
os.makedirs("plots/exp1", exist_ok=True)

plt.figure(figsize=(10,4))
plt.plot(theta_real, label="real")
plt.plot(theta_pred, label="linear model", alpha=0.7)
plt.legend()
plt.title("Model mismatch: nonlinear vs linear")
plt.show()

plt.savefig("plots/exp1/model_mismatch.png", dpi=300, bbox_inches="tight")
plt.close()