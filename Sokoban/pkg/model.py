from pkg.maze import Maze
from pkg.state import State
from pkg.coordinate import Coordinate
from pkg.action import Action
from pkg.view import View


class Model:
    """Model implementa um ambiente na forma de um labirinto com paredes e com um agente.
     A indexação da posição do agente é feita sempre por um par ordenado (lin, col). Ver classe Labirinto."""

    def __init__(self, rows, columns):
        """Construtor de modelo do ambiente físico (labirinto)
        @param rows: número de linhas do labirinto
        @param columns: número de colunas do labirinto
        """
        self.max_rows = rows
        self.max_columns = columns
        self.maze = Maze(rows,columns)
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
        elif (coordinate.col >= self.maze.max_columns or coordinate.row >= self.maze.max_rows):
            # Local está fora do modelo.
            return False
        elif self.maze.walls[coordinate.row][coordinate.col] == 1:
            # Existe uma parede no local.
            return False
        elif state.map[coordinate.row][coordinate.col] == 1:
            # Existe uma caixa no local.
            return False
        elif state.get_agent_coord() == coordinate:
            # Local onde está o agente posicionado.
            return False
        else:
            return True

    def set_agent_coord(self, row, col):
        coord = Coordinate(row, col)
        if self.check_coord(coord):
            self.current_state.set_agent(coord)
        else:
            raise ValueError("Coordenadas do agente impossível de serem atribuídas.")

    def add_element(self, row, col):
        coord = Coordinate(row, col)
        """Adiciona estado objetivo.
        @param row: linha do estado.
        @param col: coluna do estado."""
        if self.check_coord(coord):
            self.current_state.add_element(coord)
        else:
            raise ValueError("Coordenadas do elemento impossível de serem atribuídas.")

    def add_goal(self, row, col):
        coord = Coordinate(row, col)
        """Adiciona estado objetivo.
        @param row: linha do estado.
        @param col: coluna do estado."""
        if self.check_coord(coord):
            self.goal_state.add_element(coord)
        else:
            raise ValueError("Coordenadas do elemento impossível de serem atribuídas.")

    def execute(self, action):
         pass
    
    def distance_index(self, state):
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
        index = state.get_element_count() * 4
        for col in range(1, self.max_columns-1):
            for row in range(1, self.max_rows-1):
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
