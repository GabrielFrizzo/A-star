from sys import stdin, argv
from os import system, name
from state_graph import StateGraph
from maze import Maze

def clear_screen():
    if name == 'posix':
        system('clear')
    else:
        system('cls')

try:
    with open(argv[1], 'r') as file:
        graph = StateGraph(file.read())
except:
    print("Falha ao ler o arquivo, verifique o formato passado")
    exit()

clear_screen()

print("Escolha um dos algoritmos disponíveis:")
print("1 - A*")
print("2 - Busca em Aprofundamento Iterativo")

try:
    while True:
        inp = input()
        if inp == '1':
            path, cost = graph.astar()
            break
        elif inp == '2':
            path, cost = graph.deepening_search()
            break
except:
    print("Impossível encontrar um caminho")
    exit()

for maze in path:
    clear_screen()
    print(maze)
    input("Aperte ENTER para o próximo estado")
print("Custo total:", cost)
