"""Módulo principal do projeto de busca com a temática do Sokoban."""
from pkg.agent import Agent
from pkg.model import Model

if __name__ == '__main__':
    # Cria o ambiente (modelo) = Labirinto com suas paredes
    model = Model(7, 7)
    model.maze.add_vert_wall(2, 3, 4)
    model.maze.add_horiz_wall(1, 2, 4)
    # Define a posição inicial das caixas.
    model.add_element(4, 3)
    model.add_element(4, 4)
    # Define o estado objetivo.
    model.add_goal(5, 5)
    model.add_goal(1, 1)
    # Define a posição inicial do agente no ambiente - corresponde ao estado inicial
    model.set_player_coord(5, 1)

    # Cria um agente
    agent = Agent(model)

    print(f"Inicialização...\n")
    model.draw()

    # Execução...
    i = 1
    while agent.deliberate(2):
        print(f"Passo {i}...\n")
        model.draw()
        i += 1
