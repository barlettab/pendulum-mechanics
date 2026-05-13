import numpy as np
import matplotlib.pyplot as plt

from pendulum_models import simulate_simple_pendulum, simulate_double_pendulum
from metrics import entropy


# ==========================
# Simulação pêndulo simples
# ==========================

theta_simple = simulate_simple_pendulum(
    theta0=0.8,
    omega0=0,
    steps=3000
)


# ==========================
# Simulação pêndulo duplo
# ==========================

theta1, theta2 = simulate_double_pendulum(
    theta1=np.pi/2,
    theta2=np.pi/2,
    omega1=0,
    omega2=0,
    steps=3000
)


# ==========================
# calcular entropia
# ==========================

entropy_simple = entropy(theta_simple)
entropy_double = entropy(theta1)


print("Entropy - Simple Pendulum:", entropy_simple)
print("Entropy - Double Pendulum:", entropy_double)


# ==========================
# visualização
# ==========================

plt.figure(figsize=(10,4))

plt.subplot(1,2,1)
plt.hist(theta_simple, bins=50)
plt.title("Angle Distribution - Simple Pendulum")

plt.subplot(1,2,2)
plt.hist(theta1, bins=50)
plt.title("Angle Distribution - Double Pendulum")

plt.tight_layout()
plt.show()