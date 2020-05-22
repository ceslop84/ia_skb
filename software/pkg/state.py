""" Módulo que representa o estado do sistema."""
from pkg.coordinate import Coordinate

class State:
    """ Classe que representa o estado do sistema."""

    def __init__(self, max_rows, max_columns):
        """ Construtor da matriz de estado.

        Parameters:
            max_rows (int): número de linhas do labirinto
            max_columns (int): número de colunas do labirinto
        """
        self.player = Coordinate(0, 0)
        # self.max_rows = max_rows
        # self.max_columns = max_columns
        self.map = [[0 for j in range(max_columns)] for i in range(max_rows)]

    @property
    def player(self):
        """ Método tipo propriedade com a funcão GET para o campo de coordenadas do jogador.

        Returns:
            Coordinate: Objeto do tipo Coordinate.
        """
        return self.__player

    @player.setter
    def player(self, coordinate):
        """ Método tipo propriedade com a funcão SET para o campo de coordenadas do jogador.

        Parameters:
            coordinate (Coordinate): Objeto do tipo Coordinate.
        """
        self.__player = coordinate

    def add_element(self, coord):
        """ Método para adicionar novo elementos na matriz de
        elementos presentes no estados.

        Parameters:
            coord (Coordinate): Coordenadas do novo elemento.
        """
        self.map[coord.row][coord.col] = 1

    def get_element(self, coordinate):
        """ Método para recuperar elemento através de suas coordenadas.

        Returns:
            int: Valor na matriz de elementos para as coordenadas informadas.
        """
        if self.map[coordinate.row][coordinate.col] != 0:
            return self.map[coordinate.row][coordinate.col]
        else:
            return None

    def set_element(self, old_coordinate, new_coordinate):
        """ Método para substituir elemento através de suas coordenadas."""
        # Remove o elemento da posição antiga.
        self.map[old_coordinate.row][old_coordinate.col] = 0
        # Cria o elemento da nova posição.
        self.map[new_coordinate.row][new_coordinate.col] = 1

    def get_elements(self):
        """ Método para recuperar lista de elementos presentes no estado.

        Returns:
            list: Lista de elementos.
        """
        output = list()
        for col in range(len(self.map[0])):
            for row in range(len(self.map)):
                if self.map[row][col] == 1:
                    output.append(Coordinate(row, col))
        return output

    def __eq__(self, other):
        if (self.player == other.player and
                self.map == other.map):
            return True
        else:
            return False
