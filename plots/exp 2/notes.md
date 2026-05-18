Sabendo que o pêndulo simples não linear ainda mantém um comportamento periódico e previsível a longo prazo, o cenário muda radicalmente quando aumentamos os graus de liberdade do sistema. O arquivo double_pendulum.py simula o acoplamento de dois pêndulos, um sistema cujas equações diferenciais geram caos determinístico.

Se aplicarmos ângulos grandes ao modelo do pêndulo duplo, entramos no verdadeiro terreno do Efeito Borboleta. A não linearidade das equações acopla as duas hastes de tal forma que o sistema perde a periodicidade. Se rodarmos duas simulações reais idênticas, mudando apenas a posição angular inicial do segundo pêndulo em $0.0001\text{ rad}$, as duas trajetórias vão se comportar de igual maneira nos primeiros segundos, mas logo em seguida divergirão de forma irreconhecível.

Durante os primeiros 9 segundos da simulação, a distância angular entre os dois sistemas permanece cravada em zero. Mesmo sendo um sistema caótico, a divergência inicial é silenciosa e imperceptível a olho nu.

Logo após o patamar de 9 segundos, a distância angular sofre uma explosão exponencial. A perturbação minúscula de $0.001$ estoura para uma divergência macroscópica de mais de $0.5\text{ rad}$ (cerca de $28.6^\circ$). Os dois pêndulos, que começaram se movendo juntos, passam a adotar comportamentos completamente distintos e desconectados.

No Experimento 1, o erro nasce da nossa escolha de usar uma matemática simplificada (linear) para descrever a realidade não linear. No Experimento 2, o erro não é culpa de uma aproximação (ambas as trajetórias usaram a física real); o erro é uma propriedade intrínseca da natureza não linear do sistema, que amplifica incertezas.

O Efeito Borboleta prova que, para certos sistemas não lineares, mesmo que tenhamos o modelo físico perfeito, a previsão de longo prazo é impossível na prática. Como nenhum sensor no mundo real consegue medir dados com precisão infinita (sempre haverá um ruído menor que $0.001$), o erro de medição inicial inevitavelmente corromperá a previsão futura.
