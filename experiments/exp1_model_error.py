import sys
import os
import numpy as np
import matplotlib.pyplot as plt

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from models.simple_pendulum import simulate_simple_pendulum
from models.linear_simple_pendulum import simulate_linear_pendulum
from core.metrics import theils_u

# Configuração de pastas (ajustado para exp0 conforme seu código atual)
os.makedirs("data/exp0", exist_ok=True)
os.makedirs("plots/exp0", exist_ok=True)

# Ângulos solicitados em graus
angulos_graus = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90]

# Cabeçalho da tabela formatado de forma clara
print(f"{'Ângulo (°)':<12} | {'Theil\'s U':<12} | {'Período Médio Real':<20} | {'Duração Total'}")
print("-" * 70)

# Passo de tempo definido no seu backend (5ms)
dt = 0.005 

for deg in angulos_graus:
    # Conversão para radianos
    rad = np.radians(deg)
    
    # Simulações
    theta_real = simulate_simple_pendulum(rad, 0)
    theta_pred = simulate_linear_pendulum(rad, 0)
    
    # Métrica de erro
    U = theils_u(theta_real, theta_pred)
    
    # --- CÁLCULO FÍSICO DO PERÍODO DO PÊNDULO ---
    # Encontra os índices onde a onda cruza o zero subindo (mudança de sinal negativo para positivo)
    cruza_zero = np.where((theta_real[:-1] < 0) & (theta_real[1:] >= 0))[0]
    
    if len(cruza_zero) >= 2:
        # A diferença média entre cruzamentos consecutivos nos dá a quantidade de passos por ciclo
        passos_por_periodo = np.mean(np.diff(cruza_zero))
        periodo_real = passos_por_periodo * dt
        string_periodo = f"{periodo_real:.4f}s"
    else:
        string_periodo = "N/A (Ciclo incompleto)"
    # ---------------------------------------------
    
    # Tempo fixo total da janela de simulação
    tempo_total_simulado = len(theta_real) * dt
    
    # Exibe os resultados alinhados no terminal
    print(f"{deg:<12}° | {U:<12.5f} | {string_periodo:<20} | {tempo_total_simulado:.2f}s")
    
    # Salvando dados específicos de cada experimento
    np.save(f"data/exp0/theta_real_{deg}.npy", theta_real)
    np.save(f"data/exp0/theta_pred_{deg}.npy", theta_pred)
    
    # Geração do Gráfico com vetor de tempo no eixo X
    vetor_tempo = np.arange(len(theta_real)) * dt
    
    plt.figure(figsize=(10, 4))
    plt.plot(vetor_tempo, theta_real, label="Pêndulo Real (Não Linear - $\sin(\\theta)$)", color="#2ca02c", linewidth=2)
    plt.plot(vetor_tempo, theta_pred, label="Modelo Linear (Aproximação $\\theta$)", color="#d62728", linestyle="--", alpha=0.8)
    
    plt.title(f"Divergência da Dinâmica: Ângulo Inicial de {deg}°")
    plt.xlabel("Tempo (segundos)")
    plt.ylabel("Ângulo $\\theta$ (radianos)")
    plt.grid(True, linestyle=":", alpha=0.6)
    
    plt.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, -0.2),
        ncol=2,
        frameon=False
    )
    
    plt.tight_layout()
    plt.savefig(f"plots/exp1/model_mismatch_{deg}.png", dpi=300, bbox_inches="tight")
    plt.close()

print("\n✓ Todos os gráficos e dados foram salvos em 'plots/exp1/' e 'data/exp1/'.")
