O comportamento visualizado nos gráficos traduz com perfeição o impacto da simplificação matemática na modelagem de sistemas dinâmicos. A transição entre os três cenários ilustra de forma prática o limite físico da aproximação de pequenos ângulos ($\sin(\theta) \approx \theta$).

Para avaliar os limites práticos da linearização, simulamos e comparamos o comportamento de dois sistemas: um pêndulo simples real (sistema não linear governado por $\sin(\theta)$) e um modelo linearizado (aproximação por Movimento Harmônico Simples - MHS). 

O experimento consistiu em monitorar o comportamento das oscilações sob diferentes amplitudes iniciais ($\theta_0$) ao longo de 3000 passos de simulação ($dt = 0.005\text{s}$). A hipótese testada baseia-se na expansão em série de Taylor para a função seno:$$\sin(\theta) = \theta - \frac{\theta^3}{3!} + \frac{\theta^5}{5!} - \dots$$

Para valores pequenos de $\theta$, os termos de ordem superior tornam-se desprezíveis, validando a aproximação linear. No entanto, à medida que a amplitude inicial aumenta, o erro local introduzido pela omissão desses termos acumula-se a cada passo de tempo, manifestando-se como um desvio macroscópico na dinâmica global do sistema.

No primeiro gráfico, em que temos um ângulo inicial de 45° (0.8 rad), o resultado é um nítido fenômeno de descolamento de fase (Phase Drift). Em que para $\theta = 0.8$, o valor real de $\sin(0.8) \approx 0.717$, enquanto o modelo linear assume o valor cheio de $0.8$. Isso faz com que o modelo linear calcule uma força restauradora artificialmente maior do que a física real. Consequentenmente, com maior aceleração, o pêndulo linear oscila mais rápido, isto é uma frequência maior e um período menor de tempo. Visualmente, as curvas começam alinhadas, mas a curva laranja (linear) progressivamente se adianta em relação à azul (real), quebrando o sincronismo em poucos ciclos.

Entretanto, ao reduzir a amplitude inicial para o limite clássico de pequenos ângulos adotado em livros didáticos, a convergência melhora drasticamente.

É possível observar que o descolamento de fase ainda existe, mas acumula-se de forma muito mais lenta. As curvas permanecem em fase por consideráveis ciclos antes que o atraso do pêndulo real comece a se tornar perceptível a olho nu na metade final da simulação.

No cenário de estrita pequenez angular, a hipótese linear se mostra altamente eficaz. As trajetórias do modelo linear e do pêndulo real permanecem praticamente sobrepostas durante quase toda a janela temporal de simulação. O erro residual gerado pelo segundo termo da série de Taylor ($-\theta^3/3!$) torna-se pequeno o suficiente para que o desvio de fase seja irrelevante no horizonte analítico testado.

Então, o que podemos perceber é que para grandes ângulos, o período do pêndulo não depende
apenas do comprimento da corda (L) e da gravidade, o período real passa a explodir conforme o ângulo inicial aumenta.

Quando aumentamos o ângulo para $0.8\text{ rad}$ ou $1.0\text{ rad}$, o erro do modelo linear explode porque a matemática da aproximação falha. Contudo, o pêndulo real em si ainda é um sistema altamente previsível e estável. Se mudarmos a condição inicial de $0.8$ para $0.8001\text{ rad}$, o gráfico do pêndulo real mudará quase nada; ele não é sensível a pequenas perturbações. O erro que vimos é puramente erro de modelagem (inadequação do modelo linear).

Mas o que acontece se aplicarmos isso a um pêndulo duplo? É isso que vamos descobrir no experimento 2 :)

** vamos criar uma simulação de pendulo que pede o valor em do angulo em graus, daí a gente  converte para radianos e é possível verificar o que estamos falando acima, isto é,
para ângulos pequenos não importa o valor do ângulo, porém para valores maiores, o usuário
poderá verificar que existe uma mudança no período e também visualizar. Se der podemos colocar também o gráfico para ir sendo construído de forma dinâmica.

** podemos também colocar no exp1.py o tempo total que o pendulo demorará para finalizar seu movimento.
