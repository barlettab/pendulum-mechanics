"""
Comparação do horizonte de previsibilidade
Pêndulo simples vs pêndulo duplo
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import numpy as np
import matplotlib.pyplot as plt

from models.simple_pendulum import simulate_simple_pendulum
from models.double_pendulum import simulate_double_pendulum
from core.metrics import theils_u

# ==========================
# parâmetros
# ==========================
dt = 0.005

# ==========================
# criar pastas
# ==========================
os.makedirs("data/exp5", exist_ok=True)
os.makedirs("plots/exp5", exist_ok=True)

# ==========================
# simulações
# ==========================
theta_simple = simulate_simple_pendulum(0.8, 0)
theta_double = simulate_double_pendulum(np.pi/2, np.pi/2, 0, 0)[0]

# ==========================
# horizontes
# ==========================
horizons = np.arange(1, 501)
horizons_time = horizons * dt

scores_simple = []
scores_double = []

# ==========================
# análise
# ==========================
for h in horizons:

    # simples
    real_s = theta_simple[h:]
    pred_s = theta_simple[:-h]

    scores_simple.append(theils_u(real_s, pred_s))

    # duplo
    real_d = theta_double[h:]
    pred_d = theta_double[:-h]

    scores_double.append(theils_u(real_d, pred_d))

scores_simple = np.array(scores_simple)
scores_double = np.array(scores_double)

# ==========================
# salvar dados
# ==========================
np.save("data/exp5/theta_simple.npy", theta_simple)
np.save("data/exp5/theta_double.npy", theta_double)

np.save("data/exp5/horizons.npy", horizons)
np.save("data/exp5/horizons_time.npy", horizons_time)

np.save("data/exp5/scores_simple.npy", scores_simple)
np.save("data/exp5/scores_double.npy", scores_double)

# ==========================
# plot
# ==========================
plt.figure(figsize=(10,5))

plt.plot(horizons_time, scores_simple, label="Pêndulo Simples")
plt.plot(horizons_time, scores_double, label="Pêndulo Duplo")

plt.axhline(1, linestyle="--", label="U = 1 (limite)", color='red')

plt.xlabel("Forecast do Horizonte (s)")
plt.ylabel("Theil's U")

plt.title("Horizonte de Previsão: Simples vs Pêndulo Duplo")

plt.legend(
    loc="lower center",
    bbox_to_anchor=(0.5, -0.25),
    ncol=3,
    frameon=False
)
plt.grid(alpha=0.3)

plt.savefig(
    "plots/exp5/predictability_comparison.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()
