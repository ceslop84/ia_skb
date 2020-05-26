"""Módulo principal do projeto de busca com a temática do Sokoban."""
import sys
from copy import deepcopy
from os import mkdir
from datetime import datetime
from pkg.agent import Agent
from pkg.model import Model

def carregar_modelo_7():
    """ Método para gerar um modelo de tamanho 7 (5x5)."""
    # Cria o ambiente (modelo) = Labirinto com suas paredes
    model7 = Model(7, 7)
    model7.maze.add_vert_wall(2, 2, 4)
    model7.maze.add_vert_wall(2, 2, 2)
    model7.maze.add_horiz_wall(1, 2, 4)
    # Define a posição inicial das caixas.
    model7.add_element(4, 3)
    model7.add_element(2, 3)
    model7.add_element(3, 4)
    # Define o estado objetivo.
    model7.add_goal(5, 5)
    model7.add_goal(1, 1)
    model7.add_goal(1, 5)
    # Define a posição inicial do agente no ambiente - corresponde ao estado inicial
    model7.set_player_coord(5, 1)
    return model7

def carregar_modelo_8():
    """ Método para gerar um modelo de tamanho 8 (6x6)."""
    # Cria o ambiente (modelo) = Labirinto com suas paredes
    model8 = Model(8, 8)
    model8.maze.add_vert_wall(2, 4, 6)
    model8.maze.add_horiz_wall(1, 3, 3)
    # Define a posição inicial das caixas.
    model8.add_element(2, 3)
    model8.add_element(3, 4)
    model8.add_element(4, 4)
    # Define o estado objetivo.
    model8.add_goal(6, 4)
    model8.add_goal(6, 5)
    model8.add_goal(6, 6)
    # Define a posição inicial do agente no ambiente - corresponde ao estado inicial
    model8.set_player_coord(6, 1)
    return model8

if __name__ == '__main__':

    model = carregar_modelo_7()
    # Registro da hora de início para a geração dos arquivos de saída em pasta específica.
    TIMESTAMP = str(datetime.today().strftime('%Y%m%d_%H%M%S'))
    mkdir(f"{TIMESTAMP}")

    # Execução...
    for i in range(3):
        model_exec = deepcopy(model)
        sys.stdout = open(f"{TIMESTAMP}//{i}.txt", "a")
        print("Inicialização...\n")
        model_exec.draw()
        agent_exec = Agent(model_exec)
        j = 1
        while agent_exec.deliberate(i):
            print(f"Passo {j}...\n")
            model_exec.draw()
            j += 1
        del model_exec, agent_exec
