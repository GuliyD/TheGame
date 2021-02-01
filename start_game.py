from main import Graph, Graphic, Game, create_moster
from rolling import roll
import classes
import monsters
from os import system, name


def clear_console():
    if name == 'nt':
        system('cls')
    else:
        system('clear')

char = classes.fighter

g = Graph.create_graph(10, 10)

game = Game()
game.place_monster(g, create_moster(monsters.GOBLIN.copy()))
char_place = game.place_char(g, char, 94)
lvl_up = classes.LvlUp(char)

lvl_up.show_hero()
Graphic.show_map(g)
while not game.game_over:
    go = input('your turn\n>>>')
    if not game.your_turn:
        clear_console()
    game.go_char(g, go, char)
    if game.win:
        game.win = False

        if lvl_up.hero['lvl'] >= 7:
            print("YOU WON")
            break
        lvl_up.lvl_up()
        [game.place_monster(g, create_moster(monsters.GOBLIN.copy())) for i in range(lvl_up.hero['lvl'])]
        print('go to next four')
        game.place_char(g, lvl_up.hero, 94)

    if not game.your_turn:
        game.enemies_turn(g)
        Graphic.show_map(g)