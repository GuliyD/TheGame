from rolling import roll
from random import randint

base_object = {'passability': True, 'object': {'avatar': 0, 'enemy': False, 'player': False}}

def create_moster(monster):
    monster['hits'] = roll(monster['hits'])

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
    game_over = False
    win = False
    your_turn = True
    monsters_indexes = []

    def del_from_graph(self, graph, index_to_del):
        graph[index_to_del][0] = base_object.copy()
        graph[index_to_del][0]['passability'] = True

    def place_monster(self, graph, monster):
        index = randint(00, 69)
        while 1:
            if graph[index][0]['passability']:
                graph[index][0]['object'] = monster
                graph[index][0]['passability'] = False
                self.monsters_indexes.append(index)
                break

    def deal_damage(self, graph, index_to_attack, damage, index_of_attacker):
        graph[index_to_attack][0]['object']['hits'] -= damage
        print(f'{graph[index_to_attack][0]["object"]["name"]} take {damage} damage')
        if graph[index_to_attack][0]['object']['hits'] <= 0:
            print('KILL')
            if graph[index_to_attack][0]['object']['player']:
                print('GAME OVER')
                self.game_over = True
                self.del_from_graph(graph, index_to_attack)
            else:
                self.del_from_graph(graph, index_to_attack)
                win = True
                for dot in graph:
                    if dot[0]['object']['enemy']:
                        win = False
                if win:
                    self.win = win
                    self.del_from_graph(graph, index_of_attacker)

        else:
            print(f"{graph[index_to_attack][0]['object']['name']} have {graph[index_to_attack][0]['object']['hits']} hp now")

    char_place = 94
    char_placed = False

    def roll_attack(self, graph, index_of_attacker, index_to_attack):
        print(f"\n{graph[index_of_attacker][0]['object']['name']} tries to attack")
        roll_d20 = roll('1d20')
        print(f'd20 = {roll_d20}')
        if not roll_d20 == 1:
            attacker_damage = graph[index_of_attacker][0]['object']['damage']

            if roll_d20 in graph[index_of_attacker][0]['object']['critical']:
                crit1 = roll(attacker_damage)
                crit2 = roll(attacker_damage)
                damage = crit1 + crit2
                print(f'crit! = {attacker_damage} + {attacker_damage} = {crit1} + {crit2}')
                self.deal_damage(graph, index_to_attack, damage, index_of_attacker)

            else:
                attack_roll = roll_d20 + graph[index_of_attacker][0]['object']['attack']
                print(f"attack = {roll_d20} + {graph[index_of_attacker][0]['object']['attack']}")
                enemy_AC = graph[index_to_attack][0]['object']['AC']

                if attack_roll >= enemy_AC:
                    damage = roll(attacker_damage)
                    print(f'damage = {attacker_damage} = {damage}')
                    self.deal_damage(graph, index_to_attack, damage, index_of_attacker)
                else:
                    print('miss')
        else:
            print('miss')

    def place_char(self, graph, char, index):
        if graph[index][0]['passability']:
            graph[index][0]['object'] = char
            graph[index][0]['passability'] = False
            self.char_place = index

    def replace_char(self, graph, char, index_to_replace):
        if graph[index_to_replace][0]['object']['enemy']:
            self.roll_attack(graph, self.char_place, index_to_replace)
        elif graph[index_to_replace][0]['passability']:
            graph[index_to_replace][0]['passability'] = True
            graph[self.char_place][0] = base_object.copy()
            self.place_char(graph, char, index_to_replace)

    def go_char(self, graph, go, char):
        try:
            if go == 'w':
                self.replace_char(graph, char, self.char_place - 10)
                self.your_turn = False
            elif go == 's':
                self.replace_char(graph, char, self.char_place + 10)
                self.your_turn = False

            if not str(self.char_place)[1] == '9':
                if go == 'd':
                    self.replace_char(graph, char, self.char_place + 1)
                    self.your_turn = False
                elif go == 'sd' or go == 'ds':
                    self.replace_char(graph, char, self.char_place + 11)
                    self.your_turn = False
                elif go == 'wd' or go == 'dw':
                    self.replace_char(graph, char, self.char_place - 9)
                    self.your_turn = False
            if not str(self.char_place)[1] == '0':

                if go == 'a':
                    self.replace_char(graph, char, self.char_place - 1)
                    self.your_turn = False
                elif go == 'as' or go == 'sa':
                    self.replace_char(graph, char, self.char_place + 9)
                    self.your_turn = False
                elif go == 'wa' or go == 'wa':
                    self.replace_char(graph, char, self.char_place - 11)
                    self.your_turn = False

        except IndexError:
            pass

    def enemy_go(self, graph, i, index_start, index_to_go):
        graph[index_to_go][0]['object'] = graph[index_start][0]['object'].copy()
        graph[index_to_go][0]['passability'] = False

        graph[index_start][0] = base_object.copy()
        graph[index_start][0]['passability'] = True
        self.your_turn = True
        self.monsters_indexes[i] = index_to_go

    def attack_hero(self, graph, monster_index, hero_index):
        pass

    def enemies_turn(self, graph):
        for i, index in enumerate(self.monsters_indexes):
            if graph[index][0]['object']['enemy']:
                place_indexes = str(index)
                if len(str(place_indexes)) == 1:
                    x = int(place_indexes)
                    y = 0

                else:
                    y = int(place_indexes[0])
                    x = int(place_indexes[1])

                char_y = int(str(self.char_place)[0])
                char_x = int(str(self.char_place)[1])

                x_master = x
                y_master = y

                if char_x > x:
                    x += 1
                elif char_x < x:
                    x -= 1

                if char_y > y:
                    y += 1
                elif char_y < y:
                    y -= 1

                index_to_go = int(str(y) + str(x))

                if graph[index_to_go][0]['passability']:
                    self.enemy_go(graph, i, index, index_to_go)

                elif graph[index_to_go][0]['object']['player']:
                    self.roll_attack(graph, index, index_to_go)

                elif graph[int(str(y) + str(x_master))][0]['passability']:
                    self.enemy_go(graph, i, index, int(str(y) + str(x_master)))

                elif graph[int(str(y_master) + str(x))][0]['passability']:
                    self.enemy_go(graph, i, index, int(str(y_master) + str(x)))








