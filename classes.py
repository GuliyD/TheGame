from rolling import roll

fighter = {
    'lvl': 1,
    'player': True,
    'max_hp': 12,
    'hits': 12,
    'hit_dice': '1d10 + 2',
    'type_of_attack': 'melee',
    'damage': '1d8',
    'critical': [20],
    'AC': 15,
    'attack': 4,
    'avatar': 'H',
    'enemy': False,
    'name': 'Adventurer'
}

def delete_dict_keys_and_make_srting(dict_keys):
    return f"{dict_keys.keys()}".replace('dict_keys(', '').replace(')', '')




class LvlUp:
    def __init__(self, hero):
        self.hero = hero

    def show_hero(self):
        print(f"now you have:\n"
              f"hp: {self.hero['hits']}\n"
              f"attack: {self.hero['attack']}\n"
              f"damage: {self.hero['damage']}\n"
              f"AC: {self.hero['AC']}\n"
              f"crit range: {self.hero['critical']}\n")

    def hero_dice_roll_plus_one(self, name_of_dice):
        dice = self.hero[name_of_dice].split(' ')
        if len(dice) == 1:
            self.hero[name_of_dice] = f'{dice} + 1'
        else:
            self.hero[name_of_dice] = f"{dice[0]} + {int(dice[2]) + 1}"

    def AC_up(self):
        self.hero['AC'] += 1

    def damage_up(self):
        self.hero_dice_roll_plus_one('damage')

    def hp_up(self):
        self.hero_dice_roll_plus_one('hit_dice')
        self.hero['max_hp'] += self.hero['lvl']

    def attack_up(self):
        self.hero['attack'] += 1

    def crit_up(self):
        self.hero['critical'] = self.hero['critical'].append(self.hero['critical'][-1] - 1)

    def sword_up(self, hero):
        self.damage_up()
        self.attack_up()

    fighter_ups_master = [
        {'AC_up': AC_up, 'hp_up': hp_up},             # 1 lvl
        {'hp_up': hp_up, 'sword_up': sword_up},       # 2 lvl
        {'AC_up': AC_up, 'hp_up': hp_up},             # 3 lvl
        {'crit_up': crit_up}                          # etc
    ]

    fighter_ups = fighter_ups_master.copy()

    def lvl_up(self):
        lvl_now = self.hero['lvl']
        can_up = [self.fighter_ups[i]for i in range(lvl_now)]

        print('what you want to up')
        tier = 1
        while 1:
            for i in range(len(can_up)):
                print(f"tier {i+1} {delete_dict_keys_and_make_srting(can_up[i])}")
            try:
                tier = int(input('firstly choose tier, and next up:\ntier>>>'))
            except ValueError:
                continue
            if tier > len(can_up) or tier <= 0:
                print('ypu cannot take that tier')
                continue
            chosen_tier = can_up[tier - 1]
            print(delete_dict_keys_and_make_srting(chosen_tier))
            up = input('\nup (write name)>>>')
            try:
                chosen_tier[up](self=self)
            except KeyError:
                print('wrong name of up')
            self.fighter_ups[tier - 1].pop(up)
            break

        self.hero['lvl'] += 1
        hit_dice = self.hero['hit_dice']
        rolled_hit_dice = roll(hit_dice)
        self.hero['max_hp'] += rolled_hit_dice
        self.hero['hits'] = self.hero['max_hp']
        print(f"you gain {hit_dice} = {rolled_hit_dice}")
        self.show_hero()





