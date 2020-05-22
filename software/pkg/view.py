class View:
    """Desenha o ambiente (o que está representado no Model) em formato texto."""
    def __init__(self, model):
        self.model = model

    def draw_row_division(self):
        print("    ", end='')
        for _ in range(self.model.maze.max_columns):
            print("+---", end='')
        print("+")

    def draw(self, state):
        if state is None:
            state = self.model.current_state
        """Desenha o labirinto representado no modelo model."""
        for row in range(self.model.maze.max_rows):
            self.draw_row_division()
            print(" {0:2d} ".format(row), end='') # Imprime número da linha

            for col in range(self.model.maze.max_columns):
                if self.model.maze.walls[row][col] == 1: 
                    print("|XXX",end='')    # Desenha parede
                elif self.model.goal_state.get_element_by_coord(row, col):
                    if state.get_agent_coord().row == row and state.get_agent_coord().col == col:
                        print("|G-A",end='')    # Desenha objetivo e Agente.
                    elif state.get_element_by_coord(row, col):
                        print("|G-B",end='')    # Desenha objetivo e caixa. 
                    else:
                        print("|  G",end='')    # Desenha objetivo
                elif state.get_agent_coord().row == row and state.get_agent_coord().col == col:
                    print("|  A",end='')    # Desenha agente
                elif state.get_element_by_coord(row, col):
                    print("|  B",end='')    # Desenha caixa.
                else:
                    print("|   ",end='')    # Desenha vazio
            print("|")
            if row == (self.model.maze.max_rows - 1):
                self.draw_row_division()