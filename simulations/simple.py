import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Garante o vínculo com as pastas core e models
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from models.simple_pendulum import simulate_simple_pendulum
from models.linear_simple_pendulum import simulate_linear_pendulum

def rodar_simulacao_comparativa():
    print("=" * 60)
    print("   SIMULADOR LADO A LADO: REAL (NÃO LINEAR) VS MODELO LINEAR")
    print("=" * 60)
    
    # Interação com o usuário
    try:
        angulo_graus = float(input("Digite o ângulo inicial em graus (Dica: tente 10, depois 45 ou 60): "))
    except ValueError:
        print("Entrada inválida. Por favor, insira um número.")
        return

    # Conversão explícita para radianos
    angulo_rad = np.radians(angulo_graus)
    print(f"\n-> Convertendo para o domínio da física: {angulo_rad:.4f} rad")
    print("-> Computando dinâmicas... A janela gráfica abrirá em instantes.")

    # Executa os modelos do seu backend
    theta_real = simulate_simple_pendulum(angulo_rad, 0)
    theta_pred = simulate_linear_pendulum(angulo_rad, 0)
    
    # Configurações de tempo baseadas no seu dt de 0.005s
    dt = 0.005  
    tempo = np.arange(len(theta_real)) * dt
    
    # Comprimento da haste para a renderização visual (1 metro)
    L = 1.0 

    # Configuração da janela (1 linha, 2 subplots lado a lado)
    fig, (ax_geo, ax_temp) = plt.subplots(1, 2, figsize=(12, 5.5))
    fig.suptitle(f"Análise de Inadequação do Modelo: Condição Inicial $\\theta_0$ = {angulo_graus}°", 
                 fontsize=14, fontweight='bold')

    # -------------------------------------------------------------------------
    # SUBPLOT 1: Espaço Geométrico (O movimento físico)
    # -------------------------------------------------------------------------
    ax_geo.set_xlim(-1.3 * L, 1.3 * L)
    ax_geo.set_ylim(-1.3 * L, 0.3 * L)
    ax_geo.set_aspect('equal')
    ax_geo.grid(True, linestyle=":", alpha=0.5)
    ax_geo.set_title("Visualização Física do Movimento")
    
    # Ponto fixo do pivô central
    ax_geo.plot(0, 0, 'ks', ms=8, label="Pivô")
    
    # Elementos visuais do Pêndulo Real (Não Linear) - Verde
    linha_real, = ax_geo.plot([], [], color='#2ca02c', lw=3, label=r"Pêndulo Real ($\sin\theta$)")
    massa_real, = ax_geo.plot([], [], 'o', color='#2ca02c', ms=14)
    
    # Elementos visuais do Modelo Linear - Vermelho Coral
    linha_linear, = ax_geo.plot([], [], color='#d62728', lw=2, linestyle='--', label=r"Modelo Linear ($\theta$)")
    massa_linear, = ax_geo.plot([], [], 'o', color='#d62728', ms=10, alpha=0.8)
    
    ax_geo.legend(loc="upper right", frameon=True, facecolor="white", edgecolor="none", framealpha=0.9)

    # -------------------------------------------------------------------------
    # SUBPLOT 2: Espaço Temporal (O Gráfico Avançando)
    # -------------------------------------------------------------------------
    ax_temp.set_xlim(0, tempo[-1])
    # Define os limites verticais em graus com 15% de folga para visualização
    ax_temp.set_ylim(-angulo_graus * 1.15, angulo_graus * 1.15)
    ax_temp.set_xlabel("Tempo (segundos)", fontsize=10)
    ax_temp.set_ylabel("Ângulo $\\theta$ (graus)", fontsize=10)
    ax_temp.grid(True, linestyle=":", alpha=0.6)
    ax_temp.set_title("Evolução do Ângulo ao Longo do Tempo")

    # Linhas que vão desenhar as trilhas no gráfico (Convertendo saída para graus na plotagem)
    trilha_real, = ax_temp.plot([], [], color='#2ca02c', lw=2)
    trilha_linear, = ax_temp.plot([], [], color='#d62728', lw=1.8, linestyle='--')
    
    # Texto dinâmico que exibe o tempo no próprio gráfico
    txt_tempo = ax_temp.text(0.05, 0.05, '', transform=ax_temp.transAxes, 
                             fontsize=10, fontweight='bold', bbox=dict(facecolor='white', alpha=0.8))

    # -------------------------------------------------------------------------
    # Lógica de Animação e Sincronismo Numérico
    # -------------------------------------------------------------------------
    # Para rodar a 50 FPS (interval=20ms), cada frame precisa avançar 0.02s de física.
    # Como seu dt é 0.005s, precisamos saltar de 4 em 4 passos (4 * 0.005s = 0.02s).
    passo_renderizacao = 4  
    frames_totais = len(theta_real) // passo_renderizacao

    def init():
        linha_real.set_data([], [])
        massa_real.set_data([], [])
        linha_linear.set_data([], [])
        massa_linear.set_data([], [])
        trilha_real.set_data([], [])
        trilha_linear.set_data([], [])
        txt_tempo.set_text('')
        return linha_real, massa_real, linha_linear, massa_linear, trilha_real, trilha_linear, txt_tempo

    def update(frame):
        # Mapeia o frame da tela para o índice real do array de dados
        idx = frame * passo_renderizacao
        
        # Proteção para o fim do array
        if idx >= len(theta_real):
            idx = len(theta_real) - 1

        # 1. Atualiza Pêndulo Real (Geometria)
        x_real = L * np.sin(theta_real[idx])
        y_real = -L * np.cos(theta_real[idx])
        linha_real.set_data([0, x_real], [0, y_real])
        massa_real.set_data([x_real], [y_real])

        # 2. Atualiza Pêndulo Linear (Geometria)
        x_linear = L * np.sin(theta_pred[idx])
        y_linear = -L * np.cos(theta_pred[idx])
        linha_linear.set_data([0, x_linear], [0, y_linear])
        massa_linear.set_data([x_linear], [y_linear])

        # 3. Atualiza as Trilhas do Gráfico Temporal (Convertendo Rad -> Graus)
        trilha_real.set_data(tempo[:idx], np.degrees(theta_real[:idx]))
        trilha_linear.set_data(tempo[:idx], np.degrees(theta_pred[:idx]))

        # 4. Atualiza o relógio digital na tela
        txt_tempo.set_text(f"Tempo: {tempo[idx]:.2f}s")

        return linha_real, massa_real, linha_linear, massa_linear, trilha_real, trilha_linear, txt_tempo

    # Dispara a renderização estável
    ani = animation.FuncAnimation(
        fig, update, frames=frames_totais,
        init_func=init, blit=True, interval=20, repeat=False
    )

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    rodar_simulacao_comparativa()
