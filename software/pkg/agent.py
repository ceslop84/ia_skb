""" Módulo para o agente de inteligência artificial."""
import time
from pkg.node import Node
from pkg.problem import Problem


UNIFORME_COST = 0
A_START_1 = 1
A_START_2 = 2

# Funções utilitárias
def build_plan(solution_node):
    """Método calcular o plano da solucão.

    Parameters:
        solution_node(Node): Objeto do tipo Node (class) com a referência à solućão obtida.

    Returns:
        list: Referência para reconstituicão da solucão, nó a nó.
    """
    depth = solution_node.depth
    solution = [0 for i in range(depth)]
    parent = solution_node

    for i in range(len(solution) - 1, -1, -1):
        solution[i] = parent.action
        parent = parent.parent
    return solution

class Agent:
    """ Classe para o agente de inteligência artificial."""

    def __init__(self, model):
        """Construtor do agente.
        @param model: Referência do ambiente onde o agente atuará."""
        self.prob = Problem(model)
        self.model = model
        # Contador de passos no plano, usado na deliberação
        self.counter = -1
        self.plan = None

    def deliberate(self, search_type):
        """ Método para deliberar sobre a solucão do problema.

        Returns:
            boolean: Indicativo para informar se a solucão foi encontrada ou não.
        """
        # Primeira chamada, realiza busca para elaborar um plano
        if self.counter == -1:
            # 0 = custo uniforme, 1 = A* índice de distãncia, 2 = A* índice de bloqueios
            self.plan = self.cheapest_first_search(search_type)

        # Nas demais chamadas, executa o plano já calculado
        self.counter += 1

        # Atingiu o estado objetivo
        if self.prob.goal_test(self.model.current_state):
            return False
        # Algo deu errado, chegou ao final do plano sem atingir o objetivo
        if self.counter >= len(self.plan):
            return False
        current_action = self.plan[self.counter]

        # Atualiza o estado atual baseando-se apenas nas suas crenças e na função sucessora
        # Não faz leitura do sensor de posição
        suc_state = self.prob.suc(self.model.current_state, current_action)
        self.model.current_state = suc_state
        return True

    def hn1(self, state):
        """Implementa uma heurísitca - número 1 - para a estratégia A*.
        No caso hn1 é a distância em coluna do estado passado com argumento até o estado objetivo.

        Parameters:
            state (State): estado para o qual se quer calcular o valor de h(n).

        Returns:
            double: valor obtido com o caĺculo da funcão HN1.
        """

        return self.model.distance_index(state)

    def hn2(self, state):
        """Implementa uma heurísitca - número 2 - para a estratégia A*.
        No caso hn2 é uma referência ao número de graus de bloqueio que
        o estado em análise apresenta.

        Parameters:
            state (State): estado para o qual se quer calcular o valor de h(n).

        Returns:
            double: valor obtido com o caĺculo da funcão HN2.
        """
        return self.model.block_index(state)

    def cheapest_first_search(self, search_type):
        """ Realiza busca com a estratégia de custo uniforme ou A* conforme escolha
        realizada na chamada.

        Parameters:
            searchType: 0 = custo uniforme, 1 = índice de distãncia, 2 = índice de bloqueios

        Returns:
            Node: plano encontrado
        """
        start_time = time.time()
        # Algoritmo de busca
        solution = None
        # Atributos para análise de desempenho
        nodes_ct = 1 # contador de nós gerados incluídos na árvore
        # nós inseridos na árvore, mas que não necessitariam porque o estado
        # já foi explorado ou por já estar na fronteira
        explored_dicarded_nodes_ct = 0
        frontier_dicarded_nodes_ct = 0
        # cria EXPLORADOS - inicialmente vazia
        explored = list()
        # cria FRONTEIRA com estado inicial
        frontier = list()

        # Instancia a raiz, sendo o estado inicial.
        root = Node(parent=None)
        root.state = self.model.current_state
        # Adiciona o estado inicial à fronteira.
        frontier.append(root)

        # Fronteira não vazia
        while len(frontier):
            sel_node = frontier.pop(0) # retira nó da fronteira
            # Teste de objetivo
            if self.prob.goal_test(sel_node.state):
                solution = sel_node
                break
            explored.append(sel_node)

            # Obtem ações possíveis para o estado selecionado para expansão
            actions = self.prob.possible_actions(self.model.maze, sel_node.state)

            for action in actions:
                if not action.is_possible(): # Ação não é possível
                    continue

                # INSERE NÓ FILHO NA ÁRVORE DE BUSCA - SEMPRE INSERE, DEPOIS
                # VERIFICA SE O INCLUI NA FRONTEIRA OU NÃO
                # Instancia o filho ligando-o ao nó selecionado (nSel)
                child = sel_node.add_child()
                # Obtem o estado sucessor pela execução da ação <act>
                suc_state = self.prob.suc(sel_node.state, action)
                child.state = suc_state
                # Insere ações no nó filho.
                child.action = action

                # Custo g(n): custo acumulado da raiz até o nó filho
                gn_child = sel_node.custo_gn + action.get_action_cost()
                if search_type == UNIFORME_COST:
                    # Deixa h(n) zerada porque é busca de custo uniforme
                    child.set_gn_hn(gn_child, 0)
                elif search_type == A_START_1:
                    child.set_gn_hn(gn_child, self.hn1(suc_state))
                elif search_type == A_START_2:
                    child.set_gn_hn(gn_child, self.hn2(suc_state))

                # INSERE NÓ FILHO NA FRONTEIRA (SE SATISFAZ CONDIÇÕES)
                # Testa se estado do nó filho foi explorado.
                already_explored = False
                for node_explored in explored:
                    if child.state == node_explored.state:
                        already_explored = True
                        break

                # Testa se estado do nó filho está na fronteira, caso esteja
                # guarda o nó existente em nFront
                node_frontier_unexplored = None
                if not already_explored:
                    for node_frontier in frontier:
                        if child.state == node_frontier.state:
                            node_frontier_unexplored = node_frontier
                            break

                # Se ainda não foi explorado
                if not already_explored:
                    # e não está na fronteira, adiciona à fronteira
                    if node_frontier_unexplored is None:
                        frontier.append(child)
                        # Ordena a fronteira pelo f(n), ascendente
                        frontier.sort(key=lambda x: x.get_fn())
                        nodes_ct += 1
                    else:
                        # Se já está na fronteira temos que ver se é melhor
                        # Nó da fronteira tem custo maior que o filho
                        if node_frontier_unexplored.get_fn() > child.get_fn():
                            # Remove nó da fronteira (pior e deve ser substituído)
                            frontier.remove(node_frontier_unexplored)
                            # Retira-se da árvore
                            node_frontier_unexplored.remove()
                            # Adiciona filho que é melhor
                            frontier.append(child)
                            # Ordena a fronteira pelo f(n), ascendente
                            frontier.sort(key=lambda x: x.get_fn())
                            # tree_nodes_ct não é incrementado por inclui o melhor e retira o pior
                        else:
                            # Conta como descartado porque o filho é pior que o nó da
                            # fronteira e foi descartado
                            frontier_dicarded_nodes_ct += 1
                else:
                    explored_dicarded_nodes_ct += 1

        if solution is not None:
            end_time = time.time()
            diff_time = end_time-start_time
            print(f"Tempo: {diff_time}s")
            print(f"Total passos: {solution.depth}")
            print(f"Custo: {solution.get_fn()}")
            print(f"Nós gerados: {nodes_ct}")
            print(f"Nós descartados: {explored_dicarded_nodes_ct}")
            print(f"Nós de fronteira descartados: {frontier_dicarded_nodes_ct}")
            print("\n")
            return build_plan(solution)
        else:
            return None
