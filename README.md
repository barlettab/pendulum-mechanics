# Pendulum Mechanics

## Checklist de rigor físico/matemático (acadêmico)

- **Modelo físico declarado**: informar equações diferenciais usadas (simples não linear, linearizado, duplo).
- **Regime de validade**: para modelo linear, explicitar que vale para pequenos ângulos.
- **Método numérico**: registrar integrador (Euler, RK4 etc.), `dt` e número de passos.
- **Comparabilidade**: garantir mesmo `dt` e horizonte para séries comparadas.
- **Métrica**: documentar variante usada de Theil's U (neste projeto: **U2 = RMSE_modelo / RMSE_naive**).
- **Estabilidade numérica**: tratar casos degenerados (ex.: denominador quase zero em métricas).
- **Conservação de energia**: sempre reportar drift relativo de energia para validar integração numérica.
- **Reprodutibilidade**: salvar parâmetros e saídas por experimento em diretórios consistentes.

## Estado atual

- `exp1_sp_linear_real.py` já roda com `dt` consistente entre modelos e usa Theil U2 com séries alinhadas.
- O runner `run_all.py` executa scripts por caminho de arquivo.
