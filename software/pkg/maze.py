""" Módulo para a geracão de labirintos do jogo Sokoban."""

class Maze:
    """ Maze representa um labirinto com paredes.
    A indexação das posições do labirinto é dada por par ordenado (linha, coluna).
    A linha inicial é zero e a linha máxima é (maxLin - 1).
    A coluna inicial é zero e a máxima é (maxCol - 1).
    """

    def __init__(self, max_rows, max_columns):
        """Construtor do labirinto
        @param max_rows: número de linhas do labirinto
        @param max_columns: número de colunas do labirinto
        """
        # self.max_rows = max_rows
        # self.max_columns = max_columns
        # Matriz que representa o labirinto sendo as posições = 0 aquelas que contêm paredes
        # Criar paredes no entorno do labirinto.
        self.walls = [[0 for j in range(max_columns)] for i in range(max_rows)]
        self.add_vert_wall(0, max_rows-1, 0)
        self.add_vert_wall(0, max_rows-1, max_rows-1)
        self.add_horiz_wall(0, max_columns-1, 0)
        self.add_horiz_wall(0, max_columns-1, max_columns-1)

    def add_horiz_wall(self, begin, end, row):
        """Constrói parede horizontal da coluna begin até a coluna end(inclusive) na linha row.
        @param begin: coluna inicial entre 0 e max_columns - 1.
        @param end: coluna final (deve ser maior que begin).
        @param row: linha onde a parede deve ser colocada."""
        if(end >= begin and
           begin >= 0 and
           end < len(self.walls[0]) and
           row >= 0 and
           row < len(self.walls)):
            for col in range(begin, end+1, 1):
                self.walls[row][col] = 1

    def add_vert_wall(self, begin, end, col):
        """Constrói parede horizontal da linha begin até a linha end(inclusive) na coluna col.
        @param begin: linha inicial entre 0 e max_rows - 1.
        @param end: linha final (deve ser maior que begin).
        @param col: coluna onde a parede deve ser colocada."""
        if(end >= begin and
           begin >= 0 and
           end < len(self.walls) and
           col >= 0 and
           col < len(self.walls[0])):
            for row in range(begin, end+1, 1):
                self.walls[row][col] = 1
