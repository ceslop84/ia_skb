from pkg.coordinate import Coordinate

class Action:


    def __init__(self, direction):
        """Construtor da matriz de estado
        @param max_rows: número de linhas do labirinto
        @param max_columns: número de colunas do labirinto
        """
        self.type = None
        self.delta_row = 0
        self.delta_col = 0
        self.element_coordinate = None
        if direction in ("Norte", "Leste", "Sul", "Oeste"):
            self.direction = direction
        else:
            raise ValueError("Direção desconhecida.")
        if direction == "Norte":
            self.delta_row = -1
        if direction == "Leste":
            self.delta_col = 1
        if direction == "Sul":
            self.delta_row = 1
        if direction == "Oeste":
            self.delta_col = -1
        
    def preview(self, coordinate):
        row = coordinate.row
        col = coordinate.col
        if self.direction == "Norte":
            row -= 1
        if self.direction == "Leste":
            col += 1
        if self.direction == "Sul":
            row += 1
        if self.direction == "Oeste":
            col -= 1
        
        return Coordinate(row, col)

    def ispossible(self):
        if self.type is None:
            return False
        elif self.type == "Mover":
            return True
        elif self.type == "Empurrar":
            return True
        else:
            raise ValueError("Ação desconhecida.")

    def push(self, coordinate):
        self.type = "Empurrar"
        self.element_coordinate = coordinate
    
    def move(self):
        self.type = "Mover"

    def get_action_cost(self):
        """Retorna o custo da ação.
        @param action:
        @return custo da ação"""
        return 1.0