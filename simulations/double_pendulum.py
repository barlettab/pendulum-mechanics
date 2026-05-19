import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Garante o vínculo com as pastas core e models do seu projeto
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

try:
    from models.double_pendulum import simulate_double_pendulum
    from models.linear_double_pendulum import simulate_linear_double_pendulum
except ImportError:
    print("Aviso: Verifique os nomes dos arquivos e funções na sua pasta 'models'.")
    raise

def rodar_simulacao_animada_dupla():
    print("=" * 60)
    print("   SIMULADOR LADO A LADO: PÊNDULO DUPLO REAL VS LINEAR")
    print("=" * 60)
    
    # Interação com o usuário para as condições iniciais
    try:
        ang_graus = float(input("Digite o ângulo inicial para AMBAS as hastes em graus (Ex: 10 ou 45): "))
    except ValueError:
        print("Entrada inválida. Por favor, insira um número.")
        return

    # Conversão explícita para radianos
    rad = np.radians(ang_graus)
    
    # Configurações de tempo padrão do projeto
    dt = 0.005  
    tempo_total = 15.0
    vetor_tempo = np.arange(0, tempo_total, dt)
    passos_necessarios = len(vetor_tempo)

    print("\n-> Computando dinâmicas acopladas... A janela gráfica abrirá em instantes.")

    # Executa os modelos do seu backend (velocidades iniciais zeradas)
    t1_real, t2_real = simulate_double_pendulum(rad, rad, 0, 0, dt=dt, steps=passos_necessarios)
    t1_lin, t2_lin = simulate_linear_double_pendulum(rad, rad, 0, 0, dt=dt, steps=passos_necessarios)
    
    # Alinhamento e fatiamento seguro de vetores
    n_pontos = min(len(vetor_tempo), len(t1_real), len(t1_lin))
    tempo = vetor_tempo[:n_pontos]
    t1_real, t2_real = t1_real[:n_pontos], t2_real[:n_pontos]
    t1_lin, t2_lin = t1_lin[:n_pontos], t2_lin[:n_pontos]
    
    # Comprimento das hastes (1.0 metro cada -> Alcance máximo = 2.0 metros)
    L1, L2 = 1.0, 1.0 
    limite_escala = (L1 + L2) * 1.15

    # Configuração da janela (1 linha, 2 subplots lado a lado)
    fig, (ax_geo, ax_temp) = plt.subplots(1, 2, figsize=(13, 6))
    fig.suptitle(f"Análise de Descolamento de Fase no Pêndulo Duplo: $\\theta_{{1,2}}$ = {ang_graus}°", 
                 fontsize=13, fontweight='bold')

    # -------------------------------------------------------------------------
    # SUBPLOT 1: Espaço Geométrico (Renderização Física das Hastes)
    # -------------------------------------------------------------------------
    ax_geo.set_xlim(-limite_escala, limite_scale := limite_escala)
    ax_geo.set_ylim(-limite_escala, (L1 + L2) * 0.3)
    ax_geo.set_aspect('equal')
    ax_geo.grid(True, linestyle="--", linewidth=0.5, color="#e0e0e0")
    ax_geo.set_title("Visualização Física do Sistema")
    
    # Pivô Fixo
    ax_geo.plot(0, 0, 'ks', ms=8, label="Pivô")
    
    # Elementos do Pêndulo Duplo Real (Verde Escuro)
    linha_real, = ax_geo.plot([], [], color='#1e4d2b', lw=3, label=r"Real ($\sin\theta$)")
    massa1_real, = ax_geo.plot([], [], 'o', color='#1e4d2b', ms=12)
    massa2_real, = ax_geo.plot([], [], 'o', color='#2e8b57', ms=10) # Haste inferior um pouco menor
    
    # Elementos do Pêndulo Duplo Linear (Vermelho Escuro)
    linha_linear, = ax_geo.plot([], [], color='#b22222', lw=2, linestyle='--', label=r"Linearizado ($\theta$)")
    massa1_linear, = ax_geo.plot([], [], 'o', color='#b22222', ms=9, alpha=0.8)
    massa2_linear, = ax_geo.plot([], [], 'o', color='#cd5c5c', ms=7, alpha=0.8)
    
    ax_geo.legend(loc="upper right", frameon=False)

    # -------------------------------------------------------------------------
    # SUBPLOT 2: Espaço Temporal (Acompanhamento do Erro da Haste Inferior θ2)
    # -------------------------------------------------------------------------
    ax_temp.set_xlim(0, tempo[-1])
    # Define limites com folga para as oscilações da articulação mais crítica
    max_ang = max(np.max(np.abs(np.degrees(t2_real))), np.max(np.abs(np.degrees(t2_lin))))
    ax_temp.set_ylim(-max_ang * 1.15, max_ang * 1.15)
    ax_temp.set_xlabel("Tempo (segundos)")
    ax_temp.set_ylabel("Ângulo $\\theta_2$ - Haste Inferior (graus)")
    ax_temp.grid(True, linestyle="--", linewidth=0.5, color="#e0e0e0")
    ax_temp.set_title("Evolução Temporal da Articulação $\\theta_2$")

    trilha_real, = ax_temp.plot([], [], color='#1e4d2b', lw=2, label="Real $\\theta_2$")
    trilha_linear, = ax_temp.plot([], [], color='#b22222', lw=1.8, linestyle='--', label="Linear $\\theta_2$")
    ax_temp.legend(loc="upper right", frameon=False)
    
    txt_tempo = ax_temp.text(0.05, 0.05, '', transform=ax_temp.transAxes, 
                             fontsize=10, fontweight='bold', 
                             bbox=dict(facecolor='white', alpha=0.8, edgecolor='#d0d0d0', boxstyle="round"))

    # -------------------------------------------------------------------------
    # Lógica de Animação e Sincronismo Numérico
    # -------------------------------------------------------------------------
    passo_renderizacao = 4  # Pula de 4 em 4 para manter estabilidade visual a 50 FPS
    frames_totais = n_pontos // passo_renderizacao

    def init():
        linha_real.set_data([], [])
        massa1_real.set_data([], [])
        massa2_real.set_data([], [])
        linha_linear.set_data([], [])
        massa1_linear.set_data([], [])
        massa2_linear.set_data([], [])
        trilha_real.set_data([], [])
        trilha_linear.set_data([], [])
        txt_tempo.set_text('')
        return (linha_real, massa1_real, massa2_real, linha_linear, 
                massa1_linear, massa2_linear, trilha_real, trilha_linear, txt_tempo)

    def update(frame):
        idx = frame * passo_renderizacao
        if idx >= n_pontos:
            idx = n_pontos - 1

        # 1. Posições Cinemáticas do Modelo Real
        x1_r = L1 * np.sin(t1_real[idx])
        y1_r = -L1 * np.cos(t1_real[idx])
        x2_r = x1_r + L2 * np.sin(t2_real[idx])
        y2_r = y1_r - L2 * np.cos(t2_real[idx])
        
        linha_real.set_data([0, x1_r, x2_r], [0, y1_r, y2_r])
        massa1_real.set_data([x1_r], [y1_r])
        massa2_real.set_data([x2_r], [y2_r])

        # 2. Posições Cinemáticas do Modelo Linearizado
        x1_l = L1 * np.sin(t1_lin[idx])
        y1_l = -L1 * np.cos(t1_lin[idx])
        x2_l = x1_l + L2 * np.sin(t2_lin[idx])
        y2_l = y1_l - L2 * np.cos(t2_lin[idx])
        
        linha_linear.set_data([0, x1_l, x2_l], [0, y1_l, y2_l])
        massa1_linear.set_data([x1_l], [y1_l])
        massa2_linear.set_data([x2_l], [y2_l])

        # 3. Atualiza Gráfico de Linha (Foco na Haste Inferior θ2, que é mais caótica)
        trilha_real.set_data(tempo[:idx], np.degrees(t2_real[:idx]))
        trilha_linear.set_data(tempo[:idx], np.degrees(t2_lin[:idx]))

        # 4. Relógio
        txt_tempo.set_text(f"Tempo: {tempo[idx]:.2f}s")

        return (linha_real, massa1_real, massa2_real, linha_linear, 
                massa1_linear, massa2_linear, trilha_real, trilha_linear, txt_tempo)

    ani = animation.FuncAnimation(
        fig, update, frames=frames_totais,
        init_func=init, blit=True, interval=20, repeat=False
    )

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    rodar_simulacao_animada_dupla()