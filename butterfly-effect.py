import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

g = 9.81
L1 = L2 = 1
m1 = m2 = 1
dt = 0.02

# condições iniciais (quase iguais)
theta1_A, theta2_A = np.pi/2, np.pi/2
theta1_B, theta2_B = np.pi/2, np.pi/2 + 0.001

omega1_A = omega2_A = 0
omega1_B = omega2_B = 0

steps = 2500

def step(theta1, theta2, omega1, omega2):

    delta = theta2 - theta1

    den1 = (m1+m2)*L1 - m2*L1*np.cos(delta)**2
    den2 = (L2/L1)*den1

    a1 = (m2*L1*omega1**2*np.sin(delta)*np.cos(delta) +
          m2*g*np.sin(theta2)*np.cos(delta) +
          m2*L2*omega2**2*np.sin(delta) -
          (m1+m2)*g*np.sin(theta1)) / den1

    a2 = (-m2*L2*omega2**2*np.sin(delta)*np.cos(delta) +
          (m1+m2)*(g*np.sin(theta1)*np.cos(delta) -
          L1*omega1**2*np.sin(delta) -
          g*np.sin(theta2))) / den2

    omega1 += a1*dt
    omega2 += a2*dt

    theta1 += omega1*dt
    theta2 += omega2*dt

    return theta1, theta2, omega1, omega2


# armazenar trajetórias
x1_A, y1_A = [], []
x2_A, y2_A = [], []

x1_B, y1_B = [], []
x2_B, y2_B = [], []

distance = []

for i in range(steps):

    theta1_A, theta2_A, omega1_A, omega2_A = step(
        theta1_A, theta2_A, omega1_A, omega2_A
    )

    theta1_B, theta2_B, omega1_B, omega2_B = step(
        theta1_B, theta2_B, omega1_B, omega2_B
    )

    x1A = L1*np.sin(theta1_A)
    y1A = -L1*np.cos(theta1_A)

    x2A = x1A + L2*np.sin(theta2_A)
    y2A = y1A - L2*np.cos(theta2_A)

    x1_A.append(x1A)
    y1_A.append(y1A)

    x2_A.append(x2A)
    y2_A.append(y2A)

    x1B = L1*np.sin(theta1_B)
    y1B = -L1*np.cos(theta1_B)

    x2B = x1B + L2*np.sin(theta2_B)
    y2B = y1B - L2*np.cos(theta2_B)

    x1_B.append(x1B)
    y1_B.append(y1B)

    x2_B.append(x2B)
    y2_B.append(y2B)

    d = np.sqrt((x2A - x2B)**2 + (y2A - y2B)**2)
    distance.append(d)


# gráfico
fig, ax = plt.subplots(figsize=(7,7), facecolor="black")
ax.set_facecolor("black")
ax.set_xlim(-2,2)
ax.set_ylim(-2,2)
ax.set_aspect("equal")
ax.axis("off")

lineA, = ax.plot([],[], 'o-', color="cyan", lw=2, markersize=6)
lineB, = ax.plot([],[], 'o-', color="orange", lw=2, markersize=6)

traceA, = ax.plot([],[], color="cyan", alpha=0.5, linestyle='dashed')
traceB, = ax.plot([],[], color="orange", alpha=0.5, linestyle="dashed")

trailA_x, trailA_y = [], []
trailB_x, trailB_y = [], []

def update(i):

    lineA.set_data([0, x1_A[i], x2_A[i]], [0, y1_A[i], y2_A[i]])
    lineB.set_data([0, x1_B[i], x2_B[i]], [0, y1_B[i], y2_B[i]])

    trailA_x.append(x2_A[i])
    trailA_y.append(y2_A[i])

    trailB_x.append(x2_B[i])
    trailB_y.append(y2_B[i])

    traceA.set_data(trailA_x, trailA_y)
    traceB.set_data(trailB_x, trailB_y)

    return lineA, lineB, traceA, traceB

ani = FuncAnimation(fig, update, frames=steps, interval=20)

plt.figure(figsize=(10,4))
plt.plot(distance)
plt.title("Trajectory Divergence (Butterfly Effect)")
plt.xlabel("time")
plt.ylabel("distance between systems")
plt.show()