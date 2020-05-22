from copy import deepcopy
from pkg.action import Action
from pkg.coordinate import Coordinate


class Problem:
    """Representação de um problema a ser resolvido por um algoritmo de busca clássica.
    A formulação do problema - instância desta classe - reside na 'mente' do agente."""

    def __init__(self, model):
        self.model = model

    def suc(self, state, action):
        """Função sucessora: recebe um estado e calcula o estado sucessor ao executar uma ação.
        @param state: estado atual.
        @param action: ação a ser realizado a partir do estado state.
        @return estado sucessor"""
        suc_state = deepcopy(state)
        if action.type == "Mover":
            # Mover o agente.
            new_agent_coord = action.preview(state.player)
            if self.model.check_coord(new_agent_coord, suc_state):
                suc_state.player = new_agent_coord

        if action.type == "Empurrar":
            # Mover a caixa.
            elem_coord = action.element_coordinate
            new_elem_coord = action.preview(elem_coord)
            if self.model.check_coord(new_elem_coord, suc_state):
                suc_state.set_element(elem_coord, new_elem_coord)
            # Mover o agente.
            new_agent_coord = action.preview(state.player)
            if self.model.check_coord(new_agent_coord, suc_state):
                suc_state.player = new_agent_coord
        return suc_state

    def possible_actions(self, maze, state):
        """Retorna as ações possíveis de serem executadas em um estado,
        desconsiderando movimentos na diagonal.
        O valor retornado é um vetor de inteiros.
        Se o valor da posição é 0 então a ação correspondente não pode ser executada
        Caso o agente possa se mover o valor da ação é 1.
        Caso o agente possa empurrar a caixa, o valor é 2.
        Exemplo: se retornar [1, 0, 0, 0] apenas a ação 0 pode ser executada, ou seja, mover para N.
        @param maze: ambiente, ou seja o labirinto
        @param state: estado atual.
        @return ações possíveis"""
        action_n = Action("Norte")
        action_l = Action("Leste")
        action_s = Action("Sul")
        action_o = Action("Oeste")
        actions = [action_n, action_l, action_s, action_o]
        walls = maze.walls
        boxes = state.map
        coordinate = state.player
        row = coordinate.row
        col = coordinate.col
        for action in actions:
            # Testa se existe caixa livre para empurrar
            # (sem parede ou outra caixa na direção da caixa).
            if (boxes[row+action.delta_row][col+action.delta_col] != 0 and
                    walls[row+action.delta_row*2][col+action.delta_col*2] == 0 and
                    boxes[row+action.delta_row*2][col+action.delta_col*2] == 0): # Norte
                action.push(Coordinate(row+action.delta_row, col+action.delta_col))
            # Testa se há parede na direção testada.
            if (walls[row+action.delta_row][col+action.delta_col] == 0 and
                    boxes[row+action.delta_row][col+action.delta_col] == 0):
                action.move()
        return actions

    def goal_test(self, current_state):
        """Testa se alcançou o estado objetivo.
        @param currentState: estado atual.
        @return True se o estado atual for igual ao estado objetivo."""
        goal = self.model.goal_state.map
        current = current_state.map
        if goal == current:
            return True
        else:
            return False
