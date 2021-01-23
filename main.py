from rolling import roll
import monsters


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
            new_dot.insert(0, {'passability': True, 'object': {'is_basic_cell': True, 'avatar': 0}})
            graph_slave.append(new_dot)

            indexes_for_del = []
            new_dot = []
        return graph_slave

    graph = create_graph.__func__(10, 10)


class Monster:
    def __init__(self, monster):
        monster['hits'] = roll(monster['hits'])
        monster['avatar'] = '?'


class Graphic:
    @staticmethod
    def show_map(graph):
        for i in range(10):
            i *= 10
            for j in range(10):
                print(graph[i + j][0]['object']['avatar'], '', end='')
            print('', end='\n')


m = Monster(monsters.GOBLIN)

G = Graph()
g = G.graph


Graphic.show_map(g)