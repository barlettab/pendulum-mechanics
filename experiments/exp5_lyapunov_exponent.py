"""
Estimativa do Expoente de Lyapunov
usando os dados do experimento butterfly
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import numpy as np
import matplotlib.pyplot as plt

from core.divergence import divergence

# saídas do experimento
os.makedirs("data/exp5", exist_ok=True)
os.makedirs("plots/exp5", exist_ok=True)

# ==========================
# carregar dados do exp4 (dependência)
# ==========================

theta1_A = np.load("data/exp4/theta1_A.npy")
theta2_A = np.load("data/exp4/theta2_A.npy")

theta1_B = np.load("data/exp4/theta1_B.npy")
theta2_B = np.load("data/exp4/theta2_B.npy")

# ==========================
# calcular divergência
# ==========================

dist = divergence(theta1_A, theta2_A, theta1_B, theta2_B)

dist[dist == 0] = 1e-12

# ==========================
# tempo (mesma escala usada antes)
# ==========================

t = np.arange(len(dist))

# ==========================
# log da divergência
# ==========================

log_dist = np.log(dist)

# ==========================
# região inicial (crescimento exponencial)
# ==========================

fit_end = int(len(t) * 0.3)

coef = np.polyfit(t[:fit_end], log_dist[:fit_end], 1)

lyapunov = coef[0]

print("Expoente de Lyapunov estimado:", lyapunov)

# ==========================
# salvar valor
# ==========================

with open("data/exp5/lyapunov.txt", "w") as f:
    f.write(f"Lyapunov exponent: {lyapunov}")

# ==========================
# gráfico
# ==========================

plt.figure(figsize=(10,4))

plt.plot(t, log_dist, label="log(distância)")

plt.plot(
    t[:fit_end],
    coef[0]*t[:fit_end] + coef[1],
    "--",
    label=f"Ajuste linear (λ = {lyapunov:.4f})"
)

plt.xlabel("Tempo (s)")
plt.ylabel("log(distância angular)")
plt.title("Estimativa do Expoente de Lyapunov")

plt.legend()

plt.savefig(
    "plots/exp5/lyapunov_estimation.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()
