from rolling import roll
import monsters
from random import randint

base_object = {'passability': True, 'object': {'avatar': 0}}

def create_moster(monster):
    monster['hits'] = roll(monster['hits'])
    monster['avatar'] = '?'

    return monster

class Graph:
    @staticmethod
    def create_graph(x, y):
        graph = []
        for x in range(10):
            for y in range(10):
                graph.append([[-1 + x, -1 + y], [0 + x, -1 + y], [1 + x, -1 + y],
                              [-1 + x, 0 + y], [1 + x, 0 + y],
                              [-1 + x, 1 + y], [0 + x, 1 + y], [1 + x, 1 + y],
                              [f'end X:{x} y:{y}']])

        new_dot = []
        indexes_for_del = []
        graph_slave = []

        for dot in graph:
            for index in range(8):
                if (dot[index][0] == -1 or dot[index][0] == 10) or (dot[index][1] == -1 or dot[index][1] == 10):
                    indexes_for_del.append(index)

            for index in range(8):
                if not (index in indexes_for_del):
                    new_dot.append(dot[index])

            new_dot.append(dot[8])
            new_dot.insert(0, base_object.copy())
            graph_slave.append(new_dot)

            indexes_for_del = []
            new_dot = []
        return graph_slave


class Graphic:
    @staticmethod
    def show_map(graph):
        for i in range(10):
            i *= 10
            for j in range(10):
                print(graph[i + j][0]['object']['avatar'], '', end='')
            print('', end='\n')


class Game:
    def place_monster(self, graph, monster):
        index = randint(00, 69)
        if graph[index][0]['passability']:
            graph[index][0]['object'] = monster
            graph[index][0]['passability'] = False

    char_place = 94
    char_placed = False

    def place_char(self, graph, char, index):
        if graph[index][0]['passability']:
            graph[index][0]['object'] = char
            graph[index][0]['passability'] = False
            self.char_place = index

    def replace_char(self, graph, char, index_to_replace):
        if graph[index_to_replace][0]['passability']:
            graph[index_to_replace][0]['passability'] = True
            graph[self.char_place][0] = base_object.copy()
            self.place_char(graph, char, index_to_replace)

    def go_char(self, graph, go, char):
        if go == 'w':
            self.replace_char(graph, char, self.char_place - 10)





