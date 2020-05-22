""" Módulo para desenho dos resultados em tela."""
from pkg.coordinate import Coordinate

class View:
    """Desenha o ambiente (o que está representado no Model) em formato texto."""
    def __init__(self, model):
        self.model = model

    def __draw_row_division(self):
        print("    ", end='')
        for _ in range(len(self.model.maze.walls[0])):
            print("+---", end='')
        print("+")

    def draw(self, state):
        """Desenha o labirinto representado no modelo model."""
        if state is None:
            state = self.model.current_state
        for row in range(len(self.model.maze.walls)):
            self.__draw_row_division()
            print(" {0:2d} ".format(row), end='') # Imprime número da linha

            for col in range(len(self.model.maze.walls[0])):
                if self.model.maze.walls[row][col] == 1:
                    print("|XXX", end='')    # Desenha parede
                elif self.model.goal_state.get_element(Coordinate(row, col)):
                    if state.player.row == row and state.player.col == col:
                        print("|G-P", end='')    # Desenha objetivo e jogador.
                    elif state.get_element(Coordinate(row, col)):
                        print("|G-B", end='')    # Desenha objetivo e caixa.
                    else:
                        print("|  G", end='')    # Desenha objetivo
                elif state.player.row == row and state.player.col == col:
                    print("|  P", end='')    # Desenha jogador
                elif state.get_element(Coordinate(row, col)):
                    print("|  B", end='')    # Desenha caixa.
                else:
                    print("|   ", end='')    # Desenha vazio
            print("|")
            if row == (len(self.model.maze.walls) - 1):
                self.__draw_row_division()
