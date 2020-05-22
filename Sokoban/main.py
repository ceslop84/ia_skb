from pkg.agent import Agent
from pkg.model import Model


def main():
    # Definição do tamanho do labirinto.
    rows = 6
    columns = 6

    # Cria o ambiente (modelo) = Labirinto com suas paredes
    model = Model(rows, columns)
    # model.maze.add_vert_wall(3,5,4)
    # model.maze.add_horiz_wall(1,2,3)
    model.maze.add_vert_wall(2,2,2)

    # Define a posição inicial do agente no ambiente - corresponde ao estado inicial
    # model.set_agent_coord(4,1)
    model.set_agent_coord(2,1)
    # Define a posição inicial das caixas.
    # model.add_element(5,2)
    # model.add_element(5,3)
    # model.add_element(2,2)
    # model.add_element(3,3)
    # model.add_element(2,4)
    # model.add_element(4,5)
    model.add_element(2,3)
    model.add_element(3,3)

    # Define o estado objetivo.
    # model.add_goal(6,1)
    # model.add_goal(6,2)
    # model.add_goal(6,3)
    # model.add_goal(6,4)
    # model.add_goal(6,5)
    # model.add_goal(6,6)
    model.add_goal(4,3)
    model.add_goal(4,4)

    # Cria um agente
    agent = Agent(model)

    model.draw()

    # Execução...
    while agent.deliberate():
        model.draw()

if __name__ == '__main__':
    main()
