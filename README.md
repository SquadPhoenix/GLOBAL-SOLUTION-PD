# Sistema de Seleção de Portfólio de Projetos 📊
Aplicação em *Python* para simular a seleção de um portfólio de projetos, maximizando o valor entregue dentro de uma capacidade limitada de horas-especialista.
O projeto aplica diferentes abordagens algorítmicas para o problema clássico da *Mochila 0/1 (Knapsack)*:
- Estratégia **Gulosa** (não garante ótimo)
- Solução **Recursiva Pura**
- Solução **Recursiva com Memoização (Top-Down)**
- **Programação Dinâmica Bottom-Up (PD)** com reconstrução do conjunto ótimo de projetos
Tudo é executado via terminal, com exemplos de casos de teste já incluídos no bloco `if __name__ == "__main__"`.
## Integrantes
    Abner de Paiva Barbosa - RM558468
    Fernando Luiz S. Antonio - RM555201
    Thomas Reichmann - RM554812
## Requisitos
- Python 3.10 ou superior
## Funcionalidades
- **Modelagem de Projetos**
  - Cada projeto é representado como uma tupla: `(nome, valor, horas_necessarias)`.
  - Exemplo:
    ```python
    ("Projeto A", 12, 4)
    ("Projeto B", 10, 3)
    ```
  - A capacidade total (C) é dada em horas-especialista.
- **Função Auxiliar**
  - `_separar_valores_horas(projetos)`
  - Separa os campos dos projetos em três listas paralelas:
    - `nomes`
    - `valores`
    - `horas`
  - Facilita a implementação das funções principais ao trabalhar diretamente com índices.
- **Estratégia Gulosa – `valor_portfolio_guloso`**
  - Ordena os projetos pela razão `valor / horas` em ordem decrescente.
  - Vai incluindo os projetos enquanto houver capacidade disponível.
  - **Vantagem:** implementação simples e rápida.
  - **Limitação:** não garante o valor ótimo em todos os casos.
- **Recursiva Pura – `valor_portfolio_recursivo`**
  - Implementa a recorrência clássica da mochila 0/1:
    - Para cada projeto, decide entre não incluir ou incluir o projeto (se couber).
  - Explora praticamente todas as combinações de inclusão/remoção.
  - **Vantagem:** didática, espelha diretamente a fórmula matemática.
  - **Limitação:** custo de tempo exponencial, inviável para muitos projetos.
- **Recursiva com Memoização (Top-Down) – `valor_portfolio_recursivo_memo`**
  - Usa a mesma ideia da recursiva pura, mas armazena resultados para subproblemas `(indice, capacidade_restante)` em um dicionário `memo`.
  - Evita recomputar problemas repetidos.
  - **Vantagem:** reduz drasticamente o tempo de execução para O(n * C).
- **Programação Dinâmica Bottom-Up – `valor_portfolio_pd`**
  - Constrói iterativamente uma **tabela (matriz)** `T` onde:
    - `T[i][c]` = melhor valor possível usando os `i` primeiros projetos, com capacidade `c`.
  - A solução ótima final está em `T[n][C]`, onde:
    - `n` = quantidade de projetos
    - `C` = capacidade máxima de horas-especialista
  - Após o preenchimento da tabela, a função faz um **backtracking** para reconstruir quais projetos foram escolhidos.
  - **Retorno:** uma tupla `(valor_otimo, lista_de_projetos_escolhidos)`.
## Estrutura do Projeto
```text
portfolio-dp/
│
├── portfolio.py # código principal com todas as funções
├── README.md # documentação do projeto (este arquivo)
└── .gitignore # arquivos/pastas ignorados (venv, cache, etc.)
```
## Como Executar 🚀
1. **Clonar o repositório:**
```bash
git clone https://github.com/SEU-USUARIO/portfolio-dp.git
cd portfolio-dp
```
2. **Executar o programa principal:**
```bash
python portfolio.py
```
O script executará alguns **casos de teste** definidos no bloco `if __name__ == "__main__":`, comparando as quatro abordagens.
## Casos de Teste Simulados
Dentro de `portfolio.py`, o bloco principal define alguns cenários, por exemplo:
```python
# Caso clássico em que o Guloso tende a falhar
# Exemplo do enunciado
projetos_exemplo = [
    ("ProjetoA", 12, 4),
    ("ProjetoB", 10, 3),
    ("ProjetoC", 7, 2),
    ("ProjetoD", 4, 3),
]
capacidade_exemplo = 10

# Caso clássico em que o Guloso tende a falhar
projetos_guloso_falha = [
    ("P1", 60, 10),  # razao 6.0
    ("P2", 100, 20), # razao 5.0
    ("P3", 120, 30), # razao 4.0
]
capacidade_falha = 50 # solução ótima é combinar P2 + P3

```
## Uso / Exemplo de Saída
Ao executar `portfolio.py`, a saída no terminal terá um formato aproximado como:
```text
-----------------------------------------
Caso 1 - Exemplo enunciado
Capacidade: 10
Projetos: ('Projeto A', 12, 4), ('Projeto B', 10, 3), ('Projeto C', 7, 2), ('Projeto D', 4, 3)
Guloso (não garante ótimo): 29
Recursivo puro (exponencial): 29
Recursivo c/ memo (Top-Down): 29
PD Bottom-Up (ótimo): 29
Projetos escolhidos (PD): ('ProjetoA', 12, 4), ('ProjetoB', 10, 3), ('ProjetoC', 7, 2)
--> Valor máximo encontrado: 29

```
Isso permite comparar o desempenho das abordagens para o mesmo conjunto de projetos e capacidade, além de visualizar **qual conjunto de projetos** compõe a solução ótima na PD.
## Estrutura / Algoritmo
**Função Auxiliar**
- `_separar_valores_horas(projetos)`
  - Entrada: lista de `(nome, valor, horas)`.
  - Saída: três listas paralelas `nomes`, `valores`, `horas`.
  - Facilita os cálculos nas funções principais trabalhando com índices inteiros.
**Estratégia Gulosa – `valor_portfolio_guloso`**
- Ordena os projetos de acordo com a razão:
  - `razao = valor / horas`
- Itera na ordem decrescente dessa razão e seleciona o projeto se houver capacidade.
- Não revisita decisões já tomadas (uma vez pulado, não volta).
**Recursiva Pura – `valor_portfolio_recursivo`**
- Define uma função recursiva `resolver(indice, capacidade_restante)`:
  - **Caso base:** `indice == 0` ou `capacidade_restante == 0` → retorna 0.
  - **Caso geral:**
    - Se `horas_projeto > capacidade_restante`:
      - só podemos não incluir esse projeto.
    - Caso contrário:
      - calcula `valor_sem` (não inclui o projeto atual).
      - calcula `valor_com` (inclui esse projeto e reduz a capacidade).
      - retorna `max(valor_sem, valor_com)`.
**Recursiva com Memoização – `valor_portfolio_recursivo_memo`**
- Utiliza um dicionário `memo (indice,capacidade_restante)`:
  - Antes de calcular `resolver(indice, capacidade_restante)`, verifica se o par está em `memo`.
  - Caso exista, apenas retorna o valor armazenado.
  - Isso transforma muitos caminhos repetidos da recursão em simples acessos de tabela.
**Programação Dinâmica Bottom-Up – `valor_portfolio_pd`**
- Cria uma matriz `T` com dimensões `(n+1) x (C+1)`:
  - `n` = número de projetos
  - `C` = capacidade máxima
- Inicializa primeira linha e primeira coluna com 0.
- Para cada projeto `i` (1..n) e capacidade `c` (0..C):
  - Se o projeto não cabe (`horas[i-1] > c`):
    - `T[i][c] = T[i-1][c]` (herda valor da linha anterior).
  - Caso contrário:
    - `valor_sem = T[i-1][c]`
    - `valor_com = valores[i-1] + T[i-1][c - horas[i-1]]`
    - `T[i][c] = max(valor_sem, valor_com)`
- Após preencher a matriz:
  - O valor ótimo está em `T[n][C]`.
  - Um passo adicional de **backtracking** percorre a tabela de trás para frente, verificando onde `T[i][c] != T[i-1][c]`.
  - Sempre que isso acontece, significa que o projeto `i-1` foi incluído, e a capacidade `c` é diminuída pelo custo daquele projeto.
  - Dessa forma, a função monta a lista `projetos_escolhidos`.
## Complexidade (Big O) por Abordagem
- **Guloso – `valor_portfolio_guloso`**
  - Tempo:
    - Ordenação: O(n log n)
    - Varredura: O(n)
    - Total: O(n log n)
  - Espaço: O(1) adicional
  - Observação: rápido, mas não garante solução ótima em geral.
- **Recursiva Pura – `valor_portfolio_recursivo`**
  - Tempo: Exponencial em `n` (aproximadamente O(2^n)).
  - Espaço: O(n) devido à profundidade máxima de recursão.
  - Observação: usada principalmente para fins didáticos/comparativos.
- **Recursiva com Memoização (Top-Down) – `valor_portfolio_recursivo_memo`**
  - Tempo: O(n * C), onde:
    - `n` = quantidade de projetos
    - `C` = capacidade máxima
  - Espaço: O(n * C) para a tabela de memo.
  - Observação: mantém a clareza da recursão com desempenho muito melhor que a recursiva pura.
- **Programação Dinâmica Bottom-Up – `valor_portfolio_pd`**
  - Tempo: O(n * C)
  - Espaço: O(n * C) (matriz completa)
  - Observação: abordagem mais previsível, muito comum em implementações de mochila em produção, e ainda permite recuperar explicitamente o **conjunto ótimo de projetos**.
## Conclusão
O projeto demonstra a aplicação de diferentes abordagens de **Programação Dinâmica** e **estratégias de busca** para o problema de seleção de portfólio de projetos sob restrição de capacidade.
- A **estratégia gulosa** oferece um resultado rápido, mas pode falhar em encontrar o valor ótimo, servindo como exemplo de abordagem ingênua.
- A solução **recursiva pura** é simples de entender, porém ineficiente para instâncias maiores.
- A **recursiva com memoização** e a **PD Bottom-Up** garantem o valor ótimo com custo de tempo O(n * C).
- A PD Bottom-Up, além disso, recupera explicitamente **quais projetos** compõem o portfólio ótimo, tornando a solução mais interpretável para tomada de decisão.
Esse comparativo permite entender, na prática, como a escolha do algoritmo impacta diretamente a eficiência e a qualidade das decisões em problemas de otimização de recursos.