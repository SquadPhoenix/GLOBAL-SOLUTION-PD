# Sistema de Seleção de Portfólio de Projetos 📊

Aplicação em Python para simular a seleção de um portfólio de projetos, maximizando o valor entregue dentro de uma capacidade limitada de horas-especialista. O projeto aplica diferentes abordagens ao problema clássico da Mochila 0/1 (Knapsack):

- Estratégia **Gulosa** (não garante ótimo)
- Solução **Recursiva Pura**
- Solução **Recursiva com Memoização (Top-Down)**
- **Programação Dinâmica Bottom-Up (PD)** com reconstrução do conjunto ótimo de projetos

Tudo é executado via terminal, com casos de teste já incluídos no bloco `if __name__ == "__main__"`.

## Integrantes

- Abner de Paiva Barbosa - RM558468  
- Fernando Luiz S. Antonio - RM555201  
- Thomas Reichmann - RM554812

## Requisitos

- Python 3.10 ou superior

## Como Executar 🚀 (Windows PowerShell)

1) Clonar o repositório e entrar na pasta:

```powershell
git clone https://github.com/nandoantonio-git/GLOBAL-SOLUTION-PD.git
cd GLOBAL-SOLUTION-PD
```

2) (Opcional) Criar e ativar um ambiente virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3) Executar o programa principal:

```powershell
python .\portfolio.py
```

O script executa casos de teste comparando as quatro abordagens.

## Estrutura do Projeto

```text
GLOBAL-SOLUTION-PD/
├── portfolio.py   # código principal com todas as funções
└── README.md      # documentação do projeto (este arquivo)
```

## Modelagem e Funções

### **Modelagem de projetos**

Cada projeto é uma tupla `(nome, valor, horas_necessarias)`. Exemplo:

```python
("Projeto A", 12, 4)
("Projeto B", 10, 3)
```

A capacidade total `C` é dada em horas-especialista.

### **Função auxiliar** `_separar_valores_horas(projetos)`

Separa os campos dos projetos em três listas paralelas: `nomes`, `valores`, `horas`. Facilita o uso por índice nas funções principais.

### **Estratégia Gulosa – `valor_portfolio_guloso`**

Ordena os projetos por `valor/horas` (decrescente) e inclui enquanto couber. Vantagem: simples e rápida. Limitação: não garante ótimo.

### **Recursiva Pura – `valor_portfolio_recursivo`**

Implementa a recorrência da mochila 0/1, explorando combinações de incluir/não incluir. Vantagem: didática. Limitação: tempo exponencial.

### **Recursiva com Memoização (Top-Down) – `valor_portfolio_recursivo_memo`**

Memoriza subproblemas `(indice, capacidade_restante)` para evitar recomputações. Desempenho: O(n·C).

### **Programação Dinâmica Bottom-Up – `valor_portfolio_pd`**

Constrói `T[i][c]` = melhor valor com os `i` primeiros projetos e capacidade `c`. Faz backtracking para recuperar a lista de projetos escolhidos. Retorno: `(valor_otimo, lista_de_projetos_escolhidos)`.

## Casos de Teste

Dentro de `portfolio.py`, o bloco principal define cenários, por exemplo:

```python
# Exemplo do enunciado
projetos_exemplo = [
    ("Projeto A", 12, 4),
    ("Projeto B", 10, 3),
    ("Projeto C", 7, 2),
    ("Projeto D", 4, 3),
]
capacidade_exemplo = 10

# Caso clássico em que o Guloso tende a falhar
projetos_guloso_falha = [
    ("P1", 60, 10),  # razão 6.0
    ("P2", 100, 20), # razão 5.0
    ("P3", 120, 30), # razão 4.0
]
capacidade_falha = 50  # solução ótima é combinar P2 + P3
```

## Saída (exemplo)

Ao executar `portfolio.py`, a saída típica se parece com:

```text
-----------------------------------------
Caso 1 - Exemplo enunciado
Capacidade: 10
Projetos: ('Projeto A', 12, 4), ('Projeto B', 10, 3), ('Projeto C', 7, 2), ('Projeto D', 4, 3)
Guloso (não garante ótimo): 29
Recursivo puro (exponencial): 29
Recursivo c/ memo (Top-Down): 29
PD Bottom-Up (ótimo): 29
Projetos escolhidos (PD): ('Projeto A', 12, 4), ('Projeto B', 10, 3), ('Projeto C', 7, 2)
--> Valor máximo encontrado: 29
```

## Estrutura do Algoritmo (resumo)

- **Auxiliar** `_separar_valores_horas`
  - Entrada: lista `(nome, valor, horas)`; Saída: `nomes`, `valores`, `horas`.

- **Guloso – `valor_portfolio_guloso`**
  - Ordena por `razao = valor / horas`; seleciona se couber; não revisita decisões.

- **Recursiva – `valor_portfolio_recursivo`**
  - `resolver(i, c)`: base `i==0` ou `c==0` → 0.
  - Caso geral: se não cabe, herda; senão, `max(sem, com)`.

- **Memoização – `valor_portfolio_recursivo_memo`**
  - Usa `memo[(i,c)]` para evitar recomputações; mesma lógica da recursiva.

- **PD Bottom-Up – `valor_portfolio_pd`**
  - Matriz `(n+1) x (C+1)`; preenche por projetos e capacidades; backtracking recupera solução.

## Complexidade (Big O)

- **Guloso**: tempo O(n log n); espaço O(1). Não garante ótimo.
- **Recursiva pura**: tempo O(2^n); espaço O(n).
- **Recursiva c/ memo**: tempo O(n·C); espaço O(n·C).
- **PD Bottom-Up**: tempo O(n·C); espaço O(n·C); permite recuperar o conjunto ótimo.

## Conclusão

O projeto demonstra, na prática, como diferentes abordagens (gulosa, recursiva, memoizada e PD) impactam desempenho e qualidade da solução no problema de seleção de portfólio sob restrição de capacidade. A PD Bottom-Up, além de ótima, recupera explicitamente quais projetos compõem o portfólio ótimo.
