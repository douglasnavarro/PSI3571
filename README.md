# Regressor 'Lata de Sardinha':

# 1. Motivação:

Aviso: Sempre que falamos em soluções ou melhorias para o metrô alguém diz: 'O problema é político. O sistema está subdimensionado. Basta o metrô ser construído e expandido no ritmo ideal e nenhum problema existiria.' E eu concordo. É verdade. Entretanto, este é o meu jeito de aliar a disciplina da Poli à solução de um problema real e que eu acredito que poderia ser utilizada por pelo menos uma pessoa: eu mesmo.

### 1.1. O problema:
- ### Como saber se o metrô estará cheio antes de sair de casa?
  - Apesar de sabermos que em certos horários (pico) o metrô certamente estará cheio, o nível de lotação varia muito de maneira difícil de determinar, pois depende muito do comportamento das pessoas. Exemplos:
    - O metrô aparenta estar mais vazio nas sextas-feiras. Talvez seja porquê muitas pessoas vão ao trabalho de carro neste dia da semana.
    - Algumas pessoas acreditam que o metrô fique mais lotado em dias de chuva.
    - Já foi observado que determinados eventos ao longo do ano fazem com o que o metrô fique bastante cheio de forma repentina (carnaval, dias de ENEM etc.)
- ### Ou seja, **é difícil estabelecer um comportamento determinístico para a lotação do metrô**. Por isso, o uso de **dados e inteligência artificial** pode ser uma solução interessante.

### 1.2. A recompensa:
Uma ferramenta capaz de prever a lotação do metrô baseada em informações de  momentos anteriores poderia ajudar:
  - A operação do metrô a agir preventivamente para atender aumentos repentinos da demanda
  - O usuário a buscar horários melhores para utilizar o transporte.

# 2. Dados:
Foram encontrados [datasets sobre a demanda](https://transparencia.metrosp.com.br/dataset/demanda) no próprio site do metrô, mas estes dados apresentam baixa granularidade. São apresentados:
  - Passageiros transportados por linha em um mês do ano
  - Entrada de passageiros por estação no mês - média dos dias úteis

Infelizmente tais dados são genéricos demais para a aplicação que desejamos implementar.

O dataset ideal traria as seguintes colunas:

    | Estação | Timestamp | Nível de lotação do trem |

Como o nível de lotação do trem não é facilmente estimado, poderiamos pré-processar um dataset com as seguintes colunas para estimar o nível de lotação:

    | Estação | Timestamp | Entradas até o timestamp | Saídas até o timestamp |

Parece inevitável, então, que deverá ser feita alguma coleta de dados.

### 2.1 Coleta:

- Intuitivamente, uma pessoa é capaz de saber se o metrô está cheio olhando para o trem e vendo através das janelas a quanidade de pessoas. De forma análoga, podemos contar o número de cabeças/faces/pessoas reconhecidas em uma imagem para estimar uma situação de trem lotado.

### 2.1.1. Linha Amarela (ViaQuatro):

- A linha amarela utiliza trens mais modernos e apresenta aos usuários, através de monitores nas estações, o nível de lotação do próximo trem:

<p align="center"><img src="https://abrilvejasp.files.wordpress.com/2016/12/monitor_lotacao.jpeg?quality=70&strip=info&w=650&strip=info"/></p>
<p align="center">Imagem exibida nos monitores</p>

Infelizmente estas imagens são apresentadas apenas nos monitores das estações. Não há qualquer informação online, a não ser o estado atual de operação das linhas (normal, paralisada, velocidade reduzida).

De todo modo, como estes níveis de lotação dos vagões são produzidos utilizando o sistema de amortecimento do trem e já foram validados com bastante tempo de uso, as imagens dos monitores são uma boa alternativa ao método de processamento de imagem para contagem de pessoas. O monitor já fornece níveis de lotação bem definidos para todo o trem.

# 3. Rede neural:

A rede neural utilizada será da classe Multi-layer Perceptron, que utiliza o algoritmo backpropagation para aprendizagem. Será realizada uma verificação utilizando a 'regra do perceptron' para **checar se os dados são linearmente separáveis.**

 - Entradas:
   - Estação:
      - Luz (0)
      - República (1)
      - Higienópolis Mackenzie (2)
      - Paulista (3)
      - Oscar Freire (4)
      - Fradique Coutinho (5)
      - Faria Lima (6)
      - Pinheiros (7)
      - Butantâ (8)
   - Timestamp em epoch (convertido de AAAA-MM-DDTHH:MM:SS)

E proverá:
 - Saída:
   - Lotação do trem em vagões, dado um timestamp futuro
    - Lotação do trem em vagões (de 1 a 6)
      - Portas 24 a 21
      - Portas 20 a 17
      - Portas 16 a 13
      - Portas 12 a 09
      - Portas 08 a 05
      - Portas 04 a 01


### 3.1 Implementação

A implementação será realizada utilizando a linguagem de programação Python e o módulo PyBrain. Inicialmente o treino será realizado apenas com uma estação.