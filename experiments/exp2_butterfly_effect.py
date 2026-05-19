import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# Garante o vínculo com as pastas core e models do seu projeto
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

try:
    from models.double_pendulum import simulate_double_pendulum
    from models.linear_double_pendulum import simulate_linear_double_pendulum
except ImportError:
    print("Aviso: Verifique os nomes dos arquivos e funções na sua pasta 'models'.")
    raise

from core.metrics import theils_u

# Criação das pastas de saída
os.makedirs("data/exp2", exist_ok=True)
os.makedirs("plots/exp2", exist_ok=True)

# Passo de tempo (5ms) e tempo total (15 segundos)
dt = 0.005
tempo_total = 15.0
vetor_tempo = np.arange(0, tempo_total, dt)
passos_necessarios = len(vetor_tempo)

# Vetor de ângulos de 5° até 45° (passo de 5°)
angulos_graus = np.arange(5, 91, 5)

# Listas para o gráfico resumo de degradação
erros_u1 = []
erros_u2 = []

# Configurações globais de estilo científico
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'font.size': 10,
    'axes.labelsize': 11,
    'axes.titlesize': 11,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'figure.titlesize': 12
})

# Paleta de cores institucional e profunda (tons escuros para alto contraste)
cor_real_1 = "#1e4d2b"   # Verde escuro (Haste 1 Real)
cor_real_2 = "#124e3f"   # Verde azulado (Haste 2 Real)
cor_lin_1 = "#b22222"    # Vermelho escuro (Haste 1 Linear)
cor_lin_2 = "#8b0000"    # Vermelho profundo (Haste 2 Linear)

print(f"{'Ângulo Inicial':<16} | {'Theil U (θ1)':<15} | {'Theil U (θ2)'}")
print("-" * 50)

# -------------------------------------------------------------------------
# LOOP DE VARREDURA: SIMULAÇÃO E PLOTAGEM DE CADA GRÁFICO
# -------------------------------------------------------------------------
for deg in angulos_graus:
    rad = np.radians(deg)
    
    # Execução do backend
    t1_real, t2_real = simulate_double_pendulum(rad, rad, 0, 0, dt=dt, steps=passos_necessarios)
    t1_lin, t2_lin = simulate_linear_double_pendulum(rad, rad, 0, 0, dt=dt, steps=passos_necessarios)
    
    # Alinhamento exato de vetores
    n_pontos = min(len(vetor_tempo), len(t1_real), len(t1_lin))
    v_tempo = vetor_tempo[:n_pontos]
    t1_real, t2_real = t1_real[:n_pontos], t2_real[:n_pontos]
    t1_lin, t2_lin = t1_lin[:n_pontos], t2_lin[:n_pontos]
    
    # Cálculo do Erro de Modelagem
    u1 = theils_u(t1_real, t1_lin)
    u2 = theils_u(t2_real, t2_lin)
    
    erros_u1.append(u1)
    erros_u2.append(u2)
    
    print(f"θ1 = θ2 = {deg:>2}°   | {u1:<15.5f} | {u2:.5f}")
    
    # Salvando os dados brutos de todos os cenários para segurança
    np.save(f"data/exp2/t1_real_{deg}deg.npy", t1_real)
    np.save(f"data/exp2/t2_real_{deg}deg.npy", t2_real)
    
    # -------------------------------------------------------------------------
    # GERAÇÃO DO GRÁFICO DE DEFLEXÃO TEMPORAL PARA O ÂNGULO ATUAL
    # -------------------------------------------------------------------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2), sharex=True)
    
    fig.suptitle(f"Resposta Temporal do Sistema: Amplitude Inicial de {deg}° ($\\theta_1=\\theta_2={deg}^\\circ$)", 
                 fontweight='bold', y=0.98)
    
    # --- Painel Esquerdo: Haste Superior (θ1) ---
    ax1.plot(v_tempo, t1_real, label=r"Real ($\sin\theta$)", color=cor_real_1, linewidth=1.8)
    ax1.plot(v_tempo, t1_lin, label=r"Linearizado ($\theta$)", color=cor_lin_1, linewidth=1.5, linestyle="--")
    ax1.set_title("Haste Superior (Articulação $\\theta_1$)")
    ax1.set_ylabel("Deflexão Angular (rad)")
    ax1.set_xlabel("Tempo $t$ (s)")
    ax1.grid(True, linestyle="--", linewidth=0.5, color="#e0e0e0")
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    
    # Caixa com métrica de erro no gráfico 1
    ax1.text(0.04, 0.06, f"Theil's $U_1$ = {u1:.4f}", transform=ax1.transAxes, 
             fontsize=9, fontweight='bold', color="#333333",
             bbox=dict(boxstyle="round,pad=0.3", facecolor="#ffffff", edgecolor="#d0d0d0", alpha=0.85))
    ax1.legend(loc="upper right", frameon=False, fontsize=9)
    
    # --- Painel Direito: Haste Inferior (θ2) ---
    ax2.plot(v_tempo, t2_real, label=r"Real ($\sin\theta$)", color=cor_real_2, linewidth=1.8)
    ax2.plot(v_tempo, t2_lin, label=r"Linearizado ($\theta$)", color=cor_lin_2, linewidth=1.5, linestyle="--")
    ax2.set_title("Haste Inferior (Articulação $\\theta_2$)")
    ax2.set_xlabel("Tempo $t$ (s)")
    ax2.grid(True, linestyle="--", linewidth=0.5, color="#e0e0e0")
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    
    # Caixa com métrica de erro no gráfico 2
    ax2.text(0.04, 0.06, f"Theil's $U_2$ = {u2:.4f}", transform=ax2.transAxes, 
             fontsize=9, fontweight='bold', color="#333333",
             bbox=dict(boxstyle="round,pad=0.3", facecolor="#ffffff", edgecolor="#d0d0d0", alpha=0.85))
    ax2.legend(loc="upper right", frameon=False, fontsize=9)
    
    plt.tight_layout()
    
    # Salva o gráfico específico deste ângulo
    plt.savefig(f"plots/exp2/pendulo_duplo_{deg}deg.png", dpi=300, bbox_inches="tight")
    plt.close()

# -------------------------------------------------------------------------
# GRÁFICO RESUMO: CURVA DE DEGRADAÇÃO GERAL
# -------------------------------------------------------------------------
plt.figure(figsize=(7, 4.5))
plt.plot(angulos_graus, erros_u1, marker='o', linestyle='-', color='#1e4d2b', linewidth=2, label='Haste Superior ($\\theta_1$)')
plt.plot(angulos_graus, erros_u2, marker='s', linestyle='--', color='#b22222', linewidth=2, label='Haste Inferior ($\\theta_2$)')

plt.title("Evolução do Erro de Modelagem (Pêndulo Duplo)", fontweight='bold', pad=15)
plt.xlabel("Amplitude Angular Inicial (graus)")
plt.ylabel("U de Theil (Métrica de Erro)")
plt.grid(True, linestyle="--", linewidth=0.5, color="#e0e0e0")
plt.xticks(angulos_graus)
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.legend(frameon=False, loc="upper left")
plt.tight_layout()

plt.savefig("plots/exp2/degradacao_theil_double_pendulum.png", dpi=300, bbox_inches="tight")
plt.close()

print("\n✓ Todos os gráficos foram salvos com sucesso!")
print("- Gráficos por ângulo: 'plots/exp2/pendulo_duplo_[X]deg.png'")
print("- Gráfico de degradação: 'plots/exp2/degradacao_theil_double_pendulum.png'")
