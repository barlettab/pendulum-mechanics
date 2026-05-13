import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.collections import LineCollection

# parâmetros físicos
g = 9.81
L1, L2 = 1, 1
m1, m2 = 1, 1
dt = 0.02

theta1, theta2 = np.pi/2, np.pi/2
omega1, omega2 = 0, 0

t1, t2 = [], []

# simulação
for i in range(3000):

    delta = theta2 - theta1

    den1 = (m1 + m2)*L1 - m2*L1*np.cos(delta)**2
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

    t1.append(theta1)
    t2.append(theta2)

# posições
x1 = L1*np.sin(t1)
y1 = -L1*np.cos(t1)

x2 = x1 + L2*np.sin(t2)
y2 = y1 - L2*np.cos(t2)

# figura
fig, ax = plt.subplots(figsize=(7,7), facecolor='black')
ax.set_facecolor('black')

ax.set_xlim(-2,2)
ax.set_ylim(-2,2)
ax.set_aspect('equal')
ax.axis('off')

# linhas do pêndulo
line, = ax.plot([], [], lw=2, color='white')
mass1, = ax.plot([], [], 'o', color='cyan', markersize=8)
mass2, = ax.plot([], [], 'o', color='orange', markersize=8)

# rastro
trail_length = 400
trail_x = []
trail_y = []

trace = ax.scatter([], [], s=2, c=[], cmap='plasma')

def update(i):

    line.set_data([0, x1[i], x2[i]],
                  [0, y1[i], y2[i]])

    mass1.set_data([x1[i]], [y1[i]])
    mass2.set_data([x2[i]], [y2[i]])

    trail_x.append(x2[i])
    trail_y.append(y2[i])

    if len(trail_x) > trail_length:
        trail_x.pop(0)
        trail_y.pop(0)

    colors = np.linspace(0,1,len(trail_x))

    trace.set_offsets(np.c_[trail_x, trail_y])
    trace.set_array(colors)

    return line, mass1, mass2, trace

ani = FuncAnimation(fig, update, frames=len(x1), interval=20)

plt.show()