"""
Sistemas mais complexos têm maior entropia?
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import numpy as np
import matplotlib.pyplot as plt

from models.simple_pendulum import simulate_simple_pendulum
from models.double_pendulum import simulate_double_pendulum
from core.entropy import entropy

# ==========================
# pasta do experimento
# ==========================
os.makedirs("data/exp5", exist_ok=True)

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
np.save("data/exp5/simple_series.npy", simple)
np.save("data/exp5/double_series.npy", double)

np.save("data/exp5/entropy_simple.npy", np.array([entropy_simple]))
np.save("data/exp5/entropy_double.npy", np.array([entropy_double]))

# ==========================
# plot
# ==========================
os.makedirs("plots/exp5", exist_ok=True)

plt.figure(figsize=(8,4))

plt.hist(simple, bins=50, alpha=0.5, label="simple", density=True)
plt.hist(double, bins=50, alpha=0.5, label="double", density=True)

plt.legend()
plt.title("Entropy comparison")

plt.xlabel("θ")
plt.ylabel("frequency")

plt.savefig("plots/exp5/entropy_comparison.png", dpi=300, bbox_inches="tight")
plt.close()