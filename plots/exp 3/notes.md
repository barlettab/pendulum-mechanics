Quando plotamos a divergência em escala logarítmica e vemos uma tendência de crescimento linear (com aquelas oscilações típicas que parecem vales), estamos diante de uma prova visual de crescimento exponencial da perturbação. 

Nos primeiros passos de simulação, a distância angular absoluta medida no espaço linear parece nula. No entanto, ao observarmos o gráfico em escala logarítmica, vemos que a separação já está acontecendo de forma geométrica desde o início. O erro inicial de $10^{-3}\text{ rad}$ flutua e se propaga de forma silenciosa nas entranhas das equações não lineares.

Os "vales" profundos observados no gráfico logarítmico (onde a linha cai bruscamente antes de subir) representam momentos geométricos onde as trajetórias caóticas temporariamente cruzam caminhos ou se aproximam no espaço de fases, logo antes de serem repelidas de novo pela dinâmica violenta do sistema.

A tendência linear de subida na escala logarítmica confirma que a divergência obedece a uma lei de potência do tipo $d(t) \approx d_0 \cdot e^{\lambda t}$, onde $\lambda > 0$ é o Expoente de Lyapunov. O coeficiente angular ($\ e^{\lambda}$) dessa tendência de subida está diretamente ligado ao famoso Expoente de Lyapunov, que mede o quão caótico um sistema é. Dessa forma, podemos constatar no gráfico que é por volta do passo 2000, o erro acumulado transiciona para a escala macroscópica, explodindo de $10^{-3}$ para mais de $10^{-1}\text{ rad}$. A partir desse ponto, o comportamento de ambos os pêndulos se torna completamente descasado.


** deixar os passos em s**
