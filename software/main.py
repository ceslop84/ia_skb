"""Módulo principal do projeto de busca com a temática do Sokoban."""
from pkg.agent import Agent
from pkg.model import Model

if __name__ == '__main__':
        # Definição do tamanho do labirinto.
    ROWS = 6
    COLUMNS = 6
    # Cria o ambiente (modelo) = Labirinto com suas paredes
    model = Model(ROWS, COLUMNS)
    model.maze.add_vert_wall(2, 2, 2)
    # Define a posição inicial do agente no ambiente - corresponde ao estado inicial
    model.set_agent_coord(2, 1)
    # Define a posição inicial das caixas.
    model.add_element(2, 3)
    model.add_element(3, 3)

    # Define o estado objetivo.
    model.add_goal(4, 3)
    model.add_goal(4, 4)

    # Cria um agente
    agent = Agent(model)

    model.draw()

    # Execução...
    while agent.deliberate():
        model.draw()
