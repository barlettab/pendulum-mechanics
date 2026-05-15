"""
Experimento 2 — Butterfly Effect

Pequenas diferenças nas condições iniciais geram grandes diferenças
na trajetória de sistemas caóticos.

Neste experimento simulamos dois pêndulos duplos quase idênticos.
A única diferença é uma perturbação minúscula no ângulo inicial.

Analisamos como a divergência entre as trajetórias cresce ao longo do tempo.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import numpy as np
import matplotlib.pyplot as plt

from models.double_pendulum import simulate_double_pendulum
from core.divergence import divergence

# ==========================
# parâmetros da simulação
# ==========================

dt = 0.005
steps = 3000

# ==========================
# criar pasta de dados
# ==========================

os.makedirs("data/exp2", exist_ok=True)

# ==========================
# simulações
# ==========================

# trajetória A (referência)
theta1_A, theta2_A = simulate_double_pendulum(
    np.pi/2, np.pi/2,
    0, 0,
    dt=dt,
    steps=steps
)

# trajetória B (pequena perturbação inicial)
theta1_B, theta2_B = simulate_double_pendulum(
    np.pi/2 + 0.001, np.pi/2,
    0, 0,
    dt=dt,
    steps=steps
)

# ==========================
# salvar dados
# ==========================

np.save("data/exp2/theta1_A.npy", theta1_A)
np.save("data/exp2/theta2_A.npy", theta2_A)

np.save("data/exp2/theta1_B.npy", theta1_B)
np.save("data/exp2/theta2_B.npy", theta2_B)

# ==========================
# análise da divergência
# ==========================

dist = divergence(theta1_A, theta2_A, theta1_B, theta2_B)

# vetor de tempo
t = np.arange(len(dist)) * dt

# ==========================
# plot
# ==========================

os.makedirs("plots/exp2", exist_ok=True)

plt.figure(figsize=(8,5))

plt.plot(t, dist)

plt.xlabel("Tempo (s)")
plt.ylabel("Distância Angular entre trajetórias (rad)")
plt.title("Butterfly Effect — Divergência entre trajetórias")

plt.savefig(
    "plots/exp2/butterfly_effect.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()
