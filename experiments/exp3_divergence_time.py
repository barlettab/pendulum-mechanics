"""
Pequenas diferenças iniciais geram grandes diferenças?
Experimento do efeito borboleta no pêndulo duplo
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import numpy as np
import matplotlib.pyplot as plt

from models.double_pendulum import simulate_double_pendulum
from core.divergence import divergence

# ==========================
# criar pastas
# ==========================
os.makedirs("data/exp3", exist_ok=True)
os.makedirs("plots/exp3", exist_ok=True)

# ==========================
# simulações
# ==========================
A = simulate_double_pendulum(np.pi/2, np.pi/2, 0, 0)

# pequena perturbação inicial
B = simulate_double_pendulum(np.pi/2 + 0.001, np.pi/2, 0, 0)

theta1_A, theta2_A = A
theta1_B, theta2_B = B

# ==========================
# salvar dados
# ==========================
np.save("data/exp3/theta1_A.npy", theta1_A)
np.save("data/exp3/theta2_A.npy", theta2_A)

np.save("data/exp3/theta1_B.npy", theta1_B)
np.save("data/exp3/theta2_B.npy", theta2_B)

# ==========================
# calcular divergência
# ==========================
dist = divergence(theta1_A, theta2_A, theta1_B, theta2_B)

# ==========================
# plot 1 — divergência normal
# ==========================
plt.figure(figsize=(10,4))

plt.plot(dist)

plt.xlabel("Tempo (s)")
plt.ylabel("Distância Angular (rad)")
plt.title("Divergência entre Trajetórias no Pêndulo Duplo")

plt.savefig(
    "plots/exp3/butterfly_divergence.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

# ==========================
# plot 2 — escala log
# ==========================
plt.figure(figsize=(10,4))

plt.plot(dist)

plt.yscale("log")

plt.xlabel("Tempo (s)")
plt.ylabel("Log da Distância Angular (rad)")
plt.title("Divergência Exponencial (Escala em log)")

plt.savefig(
    "plots/exp3/butterfly_log_divergence.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()
