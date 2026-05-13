import numpy as np
import matplotlib.pyplot as plt

from pendulum_models import simulate_double_pendulum
from metrics import theils_u


# =============================
# CONDIÇÕES INICIAIS
# =============================

theta1_a = 1.0
theta2_a = 1.0

theta1_b = 1.0001
theta2_b = 1.0


# =============================
# SIMULAÇÕES
# =============================

theta1_A, theta2_A = simulate_double_pendulum(
    theta1_a, theta2_a, 0, 0
)

theta1_B, theta2_B = simulate_double_pendulum(
    theta1_b, theta2_b, 0, 0
)


# =============================
# MEDIDA DE DIVERGÊNCIA
# =============================

distance = np.sqrt(
    (theta1_A - theta1_B)**2 +
    (theta2_A - theta2_B)**2
)


# =============================
# THEIL'S U AO LONGO DO TEMPO
# =============================

U_series = []

for t in range(20, len(theta1_A)):

    U = theils_u(
        theta1_A[:t],
        theta1_B[:t]
    )

    U_series.append(U)


# =============================
# GRÁFICOS
# =============================

fig, axs = plt.subplots(2,1, figsize=(10,8))


axs[0].plot(distance)
axs[0].set_title("Divergence Between Two Nearly Identical Double Pendulums")
axs[0].set_ylabel("Phase distance")


axs[1].plot(U_series)
axs[1].set_title("Prediction Error (Theil's U)")
axs[1].set_ylabel("Theil's U")
axs[1].set_xlabel("time step")


plt.tight_layout()
plt.show()