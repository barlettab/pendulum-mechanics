"""
Até quando conseguimos prever o sistema?
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import numpy as np
import matplotlib.pyplot as plt

from models.double_pendulum import simulate_double_pendulum
from core.metrics import theils_u

# ==========================
# pasta do experimento
# ==========================
os.makedirs("data/exp4", exist_ok=True)

# ==========================
# sistema base
# ==========================
theta = simulate_double_pendulum(np.pi/2, np.pi/2, 0, 0)[0]

# ==========================
# análise de horizonte
# ==========================
horizons = [1, 5, 10, 20, 50]
scores = []

for h in horizons:

    real = theta[h:]
    pred = theta[:-h]

    scores.append(theils_u(real, pred))


# ==========================
# salvar dados
# ==========================
np.save("data/exp4/theta_base.npy", theta)
np.save("data/exp4/horizons.npy", horizons)
np.save("data/exp4/theils_u_scores.npy", scores)


# ==========================
# plot
# ==========================
os.makedirs("plots/exp4", exist_ok=True)
plt.plot(horizons, scores, marker="o")
plt.title("Predictability horizon")
plt.xlabel("horizon")
plt.ylabel("Theil's U")

plt.savefig("plots/exp4/predictability_horizon.png", dpi=300, bbox_inches="tight")
plt.close()