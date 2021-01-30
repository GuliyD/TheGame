from main import Graph, Graphic, Game, create_moster
from rolling import roll
import classes
import monsters


input('press enter for start creating your character')
class1 = input('please select your class:\n'
               'fighter\n>>>')
how_much_monsters = int(input('how much monsters you want?\n>>>'))
class1 = classes.fighter

char = class1


all_monsters = [create_moster(monsters.GOBLIN.copy()) for i in range(how_much_monsters)]


g = Graph.create_graph(10, 10)

game = Game()
[game.place_monster(g, i) for i in all_monsters]
char_place = game.place_char(g, char, 94)




Graphic.show_map(g)
while not game.game_over:
    go = input('your turn\n>>>')
    game.go_char(g, go, char)

    if not game.your_turn:
        game.enemies_turn(g)
        Graphic.show_map(g)