"""
Sistemas mais complexos têm maior entropia?
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

from models.simple_pendulum import simulate_simple_pendulum
from models.double_pendulum import simulate_double_pendulum
from core.entropy import entropy

# ==========================
# pasta do experimento
# ==========================
os.makedirs("data/exp7", exist_ok=True)

# ==========================
# simulações
# ==========================
simple = simulate_simple_pendulum(0.8, 0)
double = simulate_double_pendulum(np.pi/2, np.pi/2, 0, 0)[0]

# ==========================
# métricas de entropia
# ==========================
entropy_simple = entropy(simple)
entropy_double = entropy(double)

print("Entropy simple:", entropy_simple)
print("Entropy double:", entropy_double)


# ==========================
# salvar dados
# ==========================
np.save("data/exp7/simple_series.npy", simple)
np.save("data/exp7/double_series.npy", double)

np.save("data/exp7/entropy_simple.npy", np.array([entropy_simple]))
np.save("data/exp7/entropy_double.npy", np.array([entropy_double]))

os.makedirs("plots/exp6", exist_ok=True)

vel_simple = np.gradient(simple)
vel_double = np.gradient(double)

fig = plt.figure(figsize=(10,8))

gs = GridSpec(2,2, height_ratios=[1,0.8])

ax1 = fig.add_subplot(gs[0,0])
ax2 = fig.add_subplot(gs[0,1])
ax3 = fig.add_subplot(gs[1,:])   # ocupa a linha inteira

# ==========================
# (A) Espaço de fase
# ==========================

ax1.scatter(
    simple,
    vel_simple,
    s=1,
    alpha=0.3,
    label="Pêndulo simples"
)

ax1.scatter(
    double,
    vel_double,
    s=1,
    alpha=0.3,
    label="Pêndulo duplo"
)

ax1.set_title("(A) Espaço de fase")
ax1.set_xlabel("θ (rad)")
ax1.set_ylabel("ω (rad/s)")

ax1.grid(alpha=0.3)

ax1.legend(loc="lower center", ncol=2)


# ==========================
# (B) Distribuição
# ==========================

ax2.hist(
    simple,
    bins=60,
    density=True,
    alpha=0.6,
    label="Pêndulo simples"
)

ax2.hist(
    double,
    bins=60,
    density=True,
    alpha=0.6,
    label="Pêndulo duplo"
)

ax2.set_title("(B) Distribuição da posição angular")
ax2.set_xlabel("θ (rad)")
ax2.set_ylabel("Densidade")

ax2.grid(alpha=0.3)

ax2.legend(loc="upper right")


# ==========================
# (C) Entropia
# ==========================

systems = ["Pêndulo simples", "Pêndulo duplo"]
values = [entropy_simple, entropy_double]

bars = ax3.bar(systems, values)

ax3.set_title("(C) Comparação da entropia")
ax3.set_ylabel("Entropia de Shannon")

ax3.grid(axis="y", alpha=0.3)

for i, v in enumerate(values):
    ax3.text(i, v + 0.02, f"{v:.3f}", ha="center")

plt.tight_layout()

plt.savefig(
    "plots/exp7/phase_space_entropy.png",
    dpi=300,
    bbox_inches="tight"
)
