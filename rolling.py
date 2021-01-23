from random import randint


def roll(roll):
    error = """roll must be like:
    1) 3d6 + 2
    2) 3d6 - 2
    4) 3d6
    5) 3d6 + 1d4 + 2 - 1 etc."""

    roll_split = roll.split()
    first_elem_split = roll_split.pop(0).split('d')
    result = sum([randint(1, int(first_elem_split[1])) for i in range(int(first_elem_split[0]))])
    for i in range(0, len(roll_split), 2):
        roll_split_elem = roll_split[i+1]
        if 'd' in roll_split_elem:
            roll_split_elem_split = roll_split_elem.split('d')
            elem_to_add = sum([randint(1, int(roll_split_elem_split[1])) for i in range(int(roll_split_elem_split[0]))])
        else:
            elem_to_add = int(roll_split_elem)

        if roll_split[i] == '+':
            result += elem_to_add
        elif roll_split[i] == '-':
            result -= elem_to_add

    return result
