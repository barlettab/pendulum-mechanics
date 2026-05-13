import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# parâmetros físicos
g = 9.81
L1 = 1
L2 = 1
m1 = 1
m2 = 1


# equações do pêndulo duplo
def double_pendulum(t, y):

    theta1, omega1, theta2, omega2 = y

    delta = theta2 - theta1

    den1 = (m1 + m2)*L1 - m2*L1*np.cos(delta)**2
    den2 = (L2/L1)*den1

    dtheta1 = omega1
    dtheta2 = omega2

    domega1 = (
        m2*L1*omega1**2*np.sin(delta)*np.cos(delta)
        + m2*g*np.sin(theta2)*np.cos(delta)
        + m2*L2*omega2**2*np.sin(delta)
        - (m1+m2)*g*np.sin(theta1)
    ) / den1

    domega2 = (
        -m2*L2*omega2**2*np.sin(delta)*np.cos(delta)
        + (m1+m2)*g*np.sin(theta1)*np.cos(delta)
        - (m1+m2)*L1*omega1**2*np.sin(delta)
        - (m1+m2)*g*np.sin(theta2)
    ) / den2

    return [dtheta1, domega1, dtheta2, domega2]


# tempo da simulação
t_span = (0, 30)
t_eval = np.linspace(0, 30, 5000)


# condições iniciais

# sistema A
y0_A = [np.pi/2, 0, np.pi/2, 0]

# sistema B (pequena diferença)
y0_B = [np.pi/2 + 0.001, 0, np.pi/2, 0]


# simulação
sol_A = solve_ivp(double_pendulum, t_span, y0_A, t_eval=t_eval)
sol_B = solve_ivp(double_pendulum, t_span, y0_B, t_eval=t_eval)


theta1_A = sol_A.y[0]
theta1_B = sol_B.y[0]


# diferença entre trajetórias
delta_theta = np.abs(theta1_A - theta1_B)


# gráfico das trajetórias
plt.figure()
plt.plot(t_eval, theta1_A, label="Sistema A")
plt.plot(t_eval, theta1_B, label="Sistema B", linestyle="--")
plt.xlabel("Tempo")
plt.ylabel("θ₁")
plt.title("Sensibilidade às Condições Iniciais")
plt.legend()
plt.show()


# gráfico da divergência
plt.figure()
plt.semilogy(t_eval, delta_theta)
plt.xlabel("Tempo")
plt.ylabel("log(|Δθ₁|)")
plt.title("Crescimento exponencial do erro")
plt.show()