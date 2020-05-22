from pkg.model import Model
from pkg.state import State
from pkg.action import Action
from pkg.node import Node
from pkg.problem import Problem
import os

UNIFORME_COST = 0
A_START_1 = 1
A_START_2 = 2

# Funções utilitárias
def buildPlan(solutionNode):
    #@TODO: Implementação do aluno
    depth = solutionNode.depth
    solution = [0 for i in range(depth)]
    parent = solutionNode

    for i in range(len(solution) - 1, -1, -1):
        solution[i] = parent.action
        parent = parent.parent
    return solution

class Agent:

    def __init__(self, model):
        """Construtor do agente.
        @param model: Referência do ambiente onde o agente atuará."""
        self.prob = Problem(model)   
        self.model = model
        # Contador de passos no plano, usado na deliberação
        self.counter = -1 

    def deliberate(self):
        # Primeira chamada, realiza busca para elaborar um plano
        if self.counter == -1: 
            self.plan = self.cheapest_first_search(2) # 0 = custo uniforme, 1 = A* com colunas, 2 = A* com dist Euclidiana

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
        @param state: estado para o qual se quer calcular o valor de h(n)."""
        # @TODO: Implementação do aluno
        return self.model.distance_index(state)
    
    def hn2(self, state):
        """Implementa uma heurísitca - número 2 - para a estratégia A*.
        No caso hn1 é a distância distância euclidiana do estado passado com argumento até o estado objetivo.
        @param state: estado para o qual se quer calcular o valor de h(n)."""
        # @TODO: Implementação do aluno
        return self.model.block_index(state)

    def cheapest_first_search(self, searchType):
        """Realiza busca com a estratégia de custo uniforme ou A* conforme escolha realizada na chamada.
        @param searchType: 0=custo uniforme, 1=A* com heurística hn1; 2=A* com hn2
        @return plano encontrado"""
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

        while len(frontier): # Fronteira não vazia

            sel_node = frontier.pop(0) # retira nó da fronteira
            # Teste de objetivo
            if self.prob.goal_test(sel_node.state):
                solution = sel_node
                break
            explored.append(sel_node)

            # Obtem ações possíveis para o estado selecionado para expansão
            actions = self.prob.possible_actions(self.model.maze, sel_node.state)
            
            for action in actions:
                if not action.ispossible(): # Ação não é possível
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
                gn_child = sel_node.gn + action.get_action_cost()
                if searchType == UNIFORME_COST:
                    child.set_gn_hn(gn_child, 0) # Deixa h(n) zerada porque é busca de custo uniforme
                elif searchType == A_START_1:
                    child.set_gn_hn(gn_child, self.hn1(suc_state))
                elif searchType == A_START_2:
                    child.set_gn_hn(gn_child, self.hn2(suc_state)) 

                # INSERE NÓ FILHO NA FRONTEIRA (SE SATISFAZ CONDIÇÕES)
                # Testa se estado do nó filho foi explorado.
                already_explored = False
                for n in explored:
                    if(child.state == n.state):
                        already_explored = True
                        break

                # Testa se estado do nó filho está na fronteira, caso esteja
                # guarda o nó existente em nFront
                node_frontier = None
                if not already_explored:
                    for n in frontier:
                        if(child.state == n.state):
                            node_frontier = n
                            break
                
                # Se ainda não foi explorado
                if not already_explored:
                    # e não está na fronteira, adiciona à fronteira
                    if node_frontier == None:
                        frontier.append(child)
                        frontier.sort(key=lambda x: x.get_fn()) # Ordena a fronteira pelo f(n), ascendente
                        nodes_ct += 1
                    else:
                        # Se já está na fronteira temos que ver se é melhor
                        if node_frontier.get_fn() > child.get_fn():       # Nó da fronteira tem custo maior que o filho
                            frontier.remove(node_frontier)              # Remove nó da fronteira (pior e deve ser substituído)
                            node_frontier.remove()                      # Retira-se da árvore 
                            frontier.append(child)                  # Adiciona filho que é melhor
                            frontier.sort(key=lambda x: x.get_fn())  # Ordena a fronteira pelo f(n), ascendente
                            # tree_nodes_ct não é incrementado por inclui o melhor e retira o pior
                        else:
                            # Conta como descartado porque o filho é pior que o nó da fronteira e foi descartado
                            frontier_dicarded_nodes_ct += 1
                else:
                    explored_dicarded_nodes_ct += 1
        
        if(solution != None):
            return buildPlan(solution)
        else:
            return None
