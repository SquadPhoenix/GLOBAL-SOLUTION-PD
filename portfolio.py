from typing import List, Tuple

# Cada projeto é uma tupla: (nome, valor, horas_necessarias)
Projeto = Tuple[str, int, int]


def _separar_valores_horas(projetos: List[Projeto]):
    """
    Função auxiliar: separa os campos dos projetos em listas paralelas.
    """
    nomes = []
    valores = []
    horas = []
    for nome, valor, carga in projetos:
        nomes.append(nome)
        valores.append(int(valor))
        horas.append(int(carga))
    return nomes, valores, horas


def valor_portfolio_guloso(capacidade: int, projetos: List[Projeto]) -> int:
    # Estratégia Gulosa

    if capacidade <= 0 or not projetos:
        return 0

    # Calcula razão valor/horas para cada projeto
    lista_gulosa = []
    for nome, valor, horas in projetos:
        if horas > 0:
            razao = float(valor) / float(horas)
            lista_gulosa.append((nome, valor, horas, razao))

    # Ordena da maior razão para a menor
    lista_gulosa.sort(key=lambda p: p[3], reverse=True)

    capacidade_restante = capacidade
    valor_total = 0

    for nome, valor, horas, razao in lista_gulosa:
        if horas <= capacidade_restante:
            valor_total += valor
            capacidade_restante -= horas

    return valor_total


def valor_portfolio_recursivo(capacidade: int, projetos: List[Projeto]) -> int:
    # Solução Recursiva Pura.

    if capacidade <= 0 or not projetos:
        return 0

    nomes, valores, horas = _separar_valores_horas(projetos)
    quantidade_projetos = len(projetos)

    def resolver(indice: int, capacidade_restante: int) -> int:

        if indice == 0 or capacidade_restante == 0:
            return 0

        # Projeto atual é o de índice indice-1 nas listas
        horas_projeto = horas[indice - 1]
        valor_projeto = valores[indice - 1]

        # Se não cabe incluir este projeto, só podemos ignorá-lo
        if horas_projeto > capacidade_restante:
            return resolver(indice - 1, capacidade_restante)

        # Caso geral: máximo entre não incluir e incluir o projeto
        valor_sem = resolver(indice - 1, capacidade_restante)
        valor_com = valor_projeto + resolver(
            indice - 1,
            capacidade_restante - horas_projeto
        )
        if valor_com > valor_sem:
            return valor_com
        return valor_sem

    return resolver(quantidade_projetos, capacidade)


def valor_portfolio_recursivo_memo(capacidade: int, projetos: List[Projeto]) -> int:

    # Programação Dinâmica Top-Down (Recursiva com Memoização).

    if capacidade <= 0 or not projetos:
        return 0

    nomes, valores, horas = _separar_valores_horas(projetos)
    quantidade_projetos = len(projetos)
    memo = {}  # chave: (indice, capacidade_restante) -> valor máximo

    def resolver(indice: int, capacidade_restante: int) -> int:
        if (indice, capacidade_restante) in memo:
            return memo[(indice, capacidade_restante)]

        if indice == 0 or capacidade_restante == 0:
            memo[(indice, capacidade_restante)] = 0
            return 0

        horas_projeto = horas[indice - 1]
        valor_projeto = valores[indice - 1]

        if horas_projeto > capacidade_restante:
            resultado = resolver(indice - 1, capacidade_restante)
        else:
            valor_sem = resolver(indice - 1, capacidade_restante)
            valor_com = valor_projeto + resolver(
                indice - 1,
                capacidade_restante - horas_projeto
            )
            if valor_com > valor_sem:
                resultado = valor_com
            else:
                resultado = valor_sem

        memo[(indice, capacidade_restante)] = resultado
        return resultado

    return resolver(quantidade_projetos, capacidade)


def valor_portfolio_pd(capacidade: int, projetos: List[Projeto]):

    # Programação Dinâmica Bottom-Up (Iterativa) com reconstrução da solução.

    if capacidade <= 0 or not projetos:
        return 0, []

    nomes, valores, horas = _separar_valores_horas(projetos)
    quantidade_projetos = len(projetos)

    # Cria matriz (n+1) x (capacidade+1) inicializada com 0
    # T[i][c] = melhor valor usando os i primeiros projetos com capacidade c
    T = []
    for _ in range(quantidade_projetos + 1):
        linha = [0] * (capacidade + 1)
        T.append(linha)

    # Preenche a tabela linha por linha
    for i in range(1, quantidade_projetos + 1):
        for cap in range(0, capacidade + 1):
            horas_projeto = horas[i - 1]
            valor_projeto = valores[i - 1]

            # Caso em que o projeto não cabe na capacidade cap
            if horas_projeto > cap:
                T[i][cap] = T[i - 1][cap]
            else:
                valor_sem = T[i - 1][cap]
                valor_com = valor_projeto + T[i - 1][cap - horas_projeto]

                if valor_com > valor_sem:
                    T[i][cap] = valor_com
                else:
                    T[i][cap] = valor_sem

    # Valor ótimo está na última célula
    valor_otimo = T[quantidade_projetos][capacidade]

    # -------------------------------------------------------
    # RECONSTRUÇÃO DA SOLUÇÃO (BACKTRACKING NA TABELA T)
    # -------------------------------------------------------
    projetos_escolhidos = []
    capacidade_atual = capacidade
    i = quantidade_projetos

    # Caminha de trás para frente:
    while i > 0 and capacidade_atual > 0:
        if T[i][capacidade_atual] != T[i - 1][capacidade_atual]:
            nome_escolhido = nomes[i - 1]
            valor_escolhido = valores[i - 1]
            horas_escolhidas = horas[i - 1]
            projetos_escolhidos.append(
                (nome_escolhido, valor_escolhido, horas_escolhidas)
            )
            capacidade_atual -= horas_escolhidas
        i -= 1

    projetos_escolhidos.reverse()

    return valor_otimo, projetos_escolhidos


# --------------------------------------------------------------------
# Resumo de complexidade (Big-O)
#
# - valor_portfolio_guloso(...)
#       Tempo:  O(n log n)
#       Espaço: O(1) adicional
#
# - valor_portfolio_recursivo(...)
#       Tempo:  Exponencial em n (aprox. O(2^n))
#       Espaço: O(n) (profundidade da recursão)
#
# - valor_portfolio_recursivo_memo(...)
#       Tempo:  O(n * C)
#       Espaço: O(n * C)
#
# - valor_portfolio_pd(...)
#       Tempo:  O(n * C)
#       Espaço: O(n * C)
#
# Onde:
#   n = quantidade de projetos
#   C = capacidade máxima (Horas-Especialista)
# --------------------------------------------------------------------


if __name__ == "__main__":
    # Casos de teste
    # Exemplo do enunciado: C = 10, Projetos A..D
    projetos_exemplo = [
        ("Projeto A", 12, 4),
        ("Projeto B", 10, 3),
        ("Projeto C", 7, 2),
        ("Projeto D", 4, 3),
    ]
    capacidade_exemplo = 10

    # Caso em que o guloso tende a falhar
    projetos_guloso_falha = [
        ("P1", 60, 10),   # razão 6.0
        ("P2", 100, 20),  # razão 5.0
        ("P3", 120, 30),  # razão 4.0
    ]
    capacidade_falha = 50

    # Outros casos livres
    projetos_pequenos = [
        ("X", 5, 4),
        ("Y", 6, 5),
        ("Z", 3, 2),
    ]
    capacidade_pequena = 5

    projetos_solo = [
        ("Grande", 100, 10),
        ("Pequeno", 20, 3),
    ]
    capacidade_solo = 3

    casos = [
        ("Exemplo enunciado",        capacidade_exemplo,     projetos_exemplo),
        ("Guloso deve falhar",       capacidade_falha,       projetos_guloso_falha),
        ("Capacidade pequena",       capacidade_pequena,     projetos_pequenos),
        ("Apenas um projeto cabe",   capacidade_solo,        projetos_solo),
    ]

    funcoes_sem_selecao = [
        (valor_portfolio_guloso,         "Guloso (não garante ótimo)"),
        (valor_portfolio_recursivo,      "Recursivo puro (exponencial)"),
        (valor_portfolio_recursivo_memo, "Recursivo c/ memo (Top-Down)"),
    ]

    def imprimir_resultado(rotulo_metodo, resultado):
        print("  " + rotulo_metodo + ": " + str(resultado))

    indice_caso = 1
    for descricao, capacidade_caso, lista_projetos in casos:
        print("\n" + "-" * 60)
        print("Caso " + str(indice_caso) + " - " + descricao)
        print("Capacidade: " + str(capacidade_caso))
        print("Projetos: " + str(lista_projetos))

        resultados = []

        # Métodos que retornam apenas o valor
        for funcao, rotulo in funcoes_sem_selecao:
            valor = funcao(capacidade_caso, lista_projetos)
            resultados.append(valor)
            imprimir_resultado(rotulo, valor)

        # Método PD que retorna valor + lista de projetos escolhidos
        valor_pd, projetos_pd = valor_portfolio_pd(capacidade_caso, lista_projetos)
        resultados.append(valor_pd)
        print("  PD Bottom-Up (ótimo): " + str(valor_pd))
        print("    Projetos escolhidos (PD): " + str(projetos_pd))

        # Destacar o melhor valor encontrado entre as abordagens
        if len(resultados) > 0:
            melhor_valor = max(resultados)
            print("  --> Valor máximo encontrado: " + str(melhor_valor))

        indice_caso += 1
