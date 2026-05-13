import numpy as np
import matplotlib.pyplot as plt

from pendulum_models import simulate_double_pendulum
from metrics import theils_u


# ==========================
# gerar trajetória real
# ==========================

theta1, theta2 = simulate_double_pendulum(
    theta1=np.pi/2,
    theta2=np.pi/2,
    omega1=0,
    omega2=0,
    steps=3000
)


# ==========================
# horizontes de previsão
# ==========================

horizons = [1, 5, 10, 20, 50]

scores = []


for h in horizons:

    real = theta1[h:]
    pred = theta1[:-h]

    score = theils_u(real, pred)

    scores.append(score)


# ==========================
# gráfico
# ==========================

plt.figure()

plt.plot(horizons, scores, marker="o")

plt.xlabel("Prediction Horizon (steps)")
plt.ylabel("Theil's U")
plt.title("Predictability Horizon - Double Pendulum")

plt.show()