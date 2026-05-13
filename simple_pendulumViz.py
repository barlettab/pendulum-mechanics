import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# -----------------------
# parâmetros físicos
# -----------------------
g = 9.81
L = 1
dt = 0.02
steps = 3000

# -----------------------
# condições iniciais
# -----------------------
theta = 0.8
omega = 0

theta_series = []

# -----------------------
# simulação
# -----------------------
for i in range(steps):

    alpha = -(g/L)*np.sin(theta)

    omega += alpha*dt
    theta += omega*dt

    theta_series.append(theta)

theta_series = np.array(theta_series)

# posição do pêndulo
x = L*np.sin(theta_series)
y = -L*np.cos(theta_series)

# -----------------------
# estilo visual
# -----------------------
plt.style.use("dark_background")

fig, ax = plt.subplots(figsize=(8,8))
ax.set_xlim(-1.3,1.3)
ax.set_ylim(-1.3,1.3)
ax.set_aspect("equal")
ax.axis("off")

# linha do pêndulo
line, = ax.plot([],[], color="#7FDBFF", lw=3)

# rastro
trail, = ax.plot([],[], "--", color="#39CCCC", lw=1.5, alpha=0.7)

# -----------------------
# gráfico interno
# -----------------------
graph = fig.add_axes([0.62,0.65,0.32,0.28])
graph.set_facecolor("black")

graph.set_xlim(0,steps)
graph.set_ylim(theta_series.min()*1.1, theta_series.max()*1.1)

graph.spines[:].set_color("#888")
graph.tick_params(colors="#888")

curve, = graph.plot([],[], color="#2ECC40", lw=2)

# -----------------------
# animação
# -----------------------
def update(i):

    # pêndulo
    line.set_data([0,x[i]],[0,y[i]])

    # rastro últimos pontos
    trail_length = 40
    start = max(0, i-trail_length)

    trail.set_data(x[start:i], y[start:i])

    # gráfico
    curve.set_data(range(i), theta_series[:i])

    return line, trail, curve

ani = FuncAnimation(
    fig,
    update,
    frames=steps,
    interval=20,
    blit=True
)

plt.show()