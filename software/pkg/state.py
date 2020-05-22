from pkg.coordinate import Coordinate

class State:
    """Representa o estado do sistema."""

    def __init__(self, max_rows, max_columns):
        """Construtor da matriz de estado
        @param max_rows: número de linhas do labirinto
        @param max_columns: número de colunas do labirinto
        """
        self.player = Coordinate(0, 0)
        # self.max_rows = max_rows
        # self.max_columns = max_columns
        self.map = [[0 for j in range(max_columns)] for i in range(max_rows)]
        self.__element_counter = 0

    @property
    def player(self):
        return self.__player

    @player.setter
    def player(self, coordinate):
        self.__player = coordinate

    def get_element_count(self):
        return self.__element_counter

    def add_element(self, coord):
        self.__element_counter += 1
        self.map[coord.row][coord.col] = 1

    def get_element_by_coord(self, row, col):
        if self.map[row][col] != 0:
            return self.map[row][col]
        else:
            return None

    def set_element(self, old_coordinate, new_coordinate):
        # Remove o elemento da posição antiga.
        self.map[old_coordinate.row][old_coordinate.col] = 0
        # Cria o elemento da nova posição.
        self.map[new_coordinate.row][new_coordinate.col] = 1

    def get_elements(self):
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
