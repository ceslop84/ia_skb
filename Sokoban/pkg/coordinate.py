class Coordinate:
    """Representa um elemtno tipo posição..
    Neste caso, é um par ordenado que representa a linha e a coluna onde se encontra o agente no labirinto."""

    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __eq__(self, other):
        if self.row == other.row and self.col == other.col:
            return True
        else:
            return False

    def __str__(self): 
        # Permite fazer um print(state) diretamente
        return "({0:d}, {1:d})".format(self.row, self.col)
    
    def distance(self, point):
        row = abs(self.row-point.row)
        col = abs(self.col-point.col)
        return row + col
    
    def direction_ns(self, point):
        if self.row - point.row > 0:
            return -1
        elif self.row - point.row <0:
            return 1
        else:
            return 0
    
    def direction_lo(self, point):
        if self.col - point.col > 0:
            return -1
        elif self.col - point.col <0:
            return +1
        else:
            return 0