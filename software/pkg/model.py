""" Módulo para o modelo (labirinto) parao jogo Sokoban."""
from pkg.maze import Maze
from pkg.state import State
from pkg.coordinate import Coordinate
from pkg.view import View


class Model:
    """ Model implementa um ambiente na forma de um labirinto com paredes e com um agente.
    A indexação da posição do agente é feita sempre por um par ordenado (lin, col).
    Ver classe Labirinto.
    """

    def __init__(self, rows, columns):
        """ Construtor de modelo do ambiente físico (labirinto).

        Parameters:
            rows (int): número de linhas do labirinto
            columns (int): número de colunas do labirinto
        """
        self.maze = Maze(rows, columns)
        self.current_state = State(rows, columns)
        self.goal_state = State(rows, columns)
        self.view = View(self)

    def draw(self, state=None):
        """Desenha o labirinto em formato texto."""
        self.view.draw(state)

    def check_coord(self, coordinate, state=None):
        """Utilizada para verificar a posiçao em relaçao ao modelo.
        @param row: a linha onde o agente será situado.
        @param col: a coluna onde o agente será situado.
        @return true se o posicionamento é possível, false se não for."""
        if state is None:
            state = self.current_state
        if (coordinate.col < 0 or coordinate.row < 0):
            # Coordenadas negativas.
            return False
        elif (coordinate.col >= len(self.maze.walls[0]) or coordinate.row >= len(self.maze.walls)):
            # Local está fora do modelo.
            return False
        elif self.maze.walls[coordinate.row][coordinate.col] == 1:
            # Existe uma parede no local.
            return False
        elif state.map[coordinate.row][coordinate.col] == 1:
            # Existe uma caixa no local.
            return False
        elif state.player == coordinate:
            # Local onde está o agente posicionado.
            return False
        else:
            return True

    def set_player_coord(self, row, col):
        """ Registra no modelo a posicão do jogador.

        Parameters:
            row (int): posicão, em linhas.
            col (int): posicão, em colunas.
        """
        coord = Coordinate(row, col)
        if self.check_coord(coord):
            self.current_state.player = coord
        else:
            raise ValueError("Coordenadas do agente impossível de serem atribuídas.")

    def add_element(self, row, col):
        """Adiciona estado objetivo.

        Parameters:
            row (int): linha do estado.
            col (int): coluna do estado.
        """

        coord = Coordinate(row, col)
        if self.check_coord(coord):
            self.current_state.add_element(coord)
        else:
            raise ValueError("Coordenadas do elemento impossível de serem atribuídas.")

    def add_goal(self, row, col):
        """Adiciona estado objetivo.

        Parameters:
            row (int): linha do estado.
            col (int): coluna do estado.
        """

        coord = Coordinate(row, col)
        if self.check_coord(coord):
            self.goal_state.add_element(coord)
        else:
            raise ValueError("Coordenadas do elemento impossível de serem atribuídas.")

    def distance_index(self, state):
        """ Método para calcular a distância em coluna do estado passado com
        argumento até o estado objetivo.

        Parameters:
            state (State): estado para o qual se quer calcular o valor de h(n).

        Returns:
            double: valor obtido com o caĺculo da funcão HN1.
        """
        goals = self.goal_state.get_elements()
        boxes = state.get_elements()
        great_dist = -1
        for box in boxes:
            for goal in goals:
                dist = goal.distance(box)
                if dist > great_dist:
                    great_dist = dist
        return great_dist

    def block_index(self, state):
        """ Método para calcular o número de graus de bloqueio que
        o estado em análise apresenta.

        Parameters:
            state (State): estado para o qual se quer calcular o valor de h(n).

        Returns:
            double: valor obtido com o caĺculo da funcão HN2.
        """
        index = len(state.get_elements()) * 4
        for col in range(1, len(self.maze.walls[0])-1):
            for row in range(1, len(self.maze.walls)-1):
                # Calcula os graus de bloqueio.
                if state.map[row][col] == 1:
                    if self.goal_state.map[row][col] == 1:
                        index -= 4
                    else:
                        if state.map[row-1][col] == 0 and self.maze.walls[row-1][col] == 0:
                            index -= 1
                        if state.map[row+1][col] == 0 and self.maze.walls[row+1][col] == 0:
                            index -= 1
                        if state.map[row][col-1] == 0 and self.maze.walls[row][col-1] == 0:
                            index -= 1
                        if state.map[row][col+1] == 0 and self.maze.walls[row][col+1] == 0:
                            index -= 1
        return index
