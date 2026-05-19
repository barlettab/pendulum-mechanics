import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# Garante o vínculo com as pastas core e models
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

try:
    from models.simple_pendulum import simulate_simple_pendulum
    from models.double_pendulum import simulate_double_pendulum
    from core.metrics import theils_u
except ImportError:
    print("Erro: Verifique os caminhos do seu backend (models/core).")
    raise

# =========================================================================
# 1. CONFIGURAÇÕES DO EXPERIMENTO
# =========================================================================
dt = 0.005
steps = 3000 # 15 segundos
tempo = np.arange(steps) * dt

os.makedirs("data/exp6", exist_ok=True)
os.makedirs("plots/exp6", exist_ok=True)

# Estilo para publicação
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'font.size': 10,
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9
})

# Ruído inevitável de leitura de um sensor real (0.057 graus)
ruido_sensor = 0.001 

print("-> Computando horizontes reais de previsibilidade...")

# =========================================================================
# 2. SIMULAÇÃO DAS TRAJETÓRIAS (Real vs Previsão com Incerteza)
# =========================================================================

# PÊNDULO SIMPLES (Alta Amplitude - 90° para ser um teste justo)
ang_inicial = np.pi / 2
simples_real = simulate_simple_pendulum(ang_inicial, 0, dt=dt, steps=steps)
simples_pred = simulate_simple_pendulum(ang_inicial + ruido_sensor, 0, dt=dt, steps=steps)

# PÊNDULO DUPLO (Haste Superior e Inferior)
duplo_t1_real, duplo_t2_real = simulate_double_pendulum(ang_inicial, ang_inicial, 0, 0, dt=dt, steps=steps)
duplo_t1_pred, duplo_t2_pred = simulate_double_pendulum(ang_inicial + ruido_sensor, ang_inicial, 0, 0, dt=dt, steps=steps)

# Garantindo alinhamento estrito dos tamanhos de array
n_pontos = min(steps, len(simples_real), len(duplo_t1_real))
tempo = tempo[:n_pontos]

# =========================================================================
# 3. ANÁLISE DO HORIZONTE DE PREVISIBILIDADE CUMULATIVO
# =========================================================================
scores_simple = []
scores_double = []

# O loop agora calcula o erro acumulado do início até o instante de tempo 'h'
for h in range(10, n_pontos):
    # Erro acumulado no pêndulo simples até o momento h
    u_s = theils_u(simples_real[:h], simples_pred[:h])
    scores_simple.append(u_s)
    
    # Erro acumulado no pêndulo duplo (média das duas hastes) até o momento h
    u_d1 = theils_u(duplo_t1_real[:h], duplo_t1_pred[:h])
    u_d2 = theils_u(duplo_t2_real[:h], duplo_t2_pred[:h])
    scores_double.append((u_d1 + u_d2) / 2.0)

horizontes_tempo = tempo[10:]

# Salvar dados brutos
np.save("data/exp6/scores_simple.npy", scores_simple)
np.save("data/exp6/scores_double.npy", scores_double)

# =========================================================================
# 4. PLOTAGEM DO GRÁFICO DEFINITIVO DO ARTIGO
# =========================================================================
fig, ax = plt.subplots(figsize=(8.5, 4.8))

ax.plot(horizontes_tempo, scores_simple, label="Pêndulo Simples (Periódico)", color='#1a5f7a', linewidth=2)
ax.plot(horizontes_tempo, scores_double, label="Pêndulo Duplo (Caótico)", color='#b22222', linewidth=2)

# Linha limite do Theil's U (U >= 1 significa que a previsão é pior que um chute estático)
ax.axhline(1.0, linestyle="--", color='#333333', alpha=0.7, label="Limite de Inutilidade ($U = 1$)")

# Formatação do layout científico
ax.set_xlabel("Horizonte de Previsão Acumulado (segundos)")
ax.set_ylabel("Erro de Previsão Relativo (Theil's $U$)")
ax.set_title("Horizonte de Previsibilidade: Sistema Estável vs Sistema Caótico", fontweight='bold', pad=12)
ax.set_xlim(0, tempo[-1])
ax.set_ylim(-0.05, 1.3)

ax.grid(True, linestyle="--", linewidth=0.5, color="#e0e0e0")
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Anotação pedagógica e visual para o leitor do artigo
ax.text(9.5, 0.85, "Explosão Caótica:\nPrevisão Impossível", color='#b22222', fontsize=9, fontweight='bold')
ax.text(9.5, 0.12, "Previsibilidade\nDeterminística", color='#1a5f7a', fontsize=9, fontweight='bold')

ax.legend(loc="upper left", frameon=False)
plt.tight_layout()

plt.savefig("plots/exp6/predictability_comparison.png", dpi=300, bbox_inches="tight")
plt.close()

print("✓ Novo gráfico gerado. Agora ele prova matematicamente a perda de previsibilidade!")
