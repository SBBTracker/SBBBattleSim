def get_support_targets(position, horn=False):
    if horn:
        return [1, 2, 3, 4]
    return {
        5: (1, 2),
        6: (2, 3),
        7: (3, 4)
    }.get(position, ())


def get_behind_targets(position):
    return {
        1: (5,),
        2: (5, 6),
        3: (6, 7),
        4: (7)
    }.get(position, ())


def get_spawn_positions(position):
    spawn_order = {
        1: (1, 2, 3, 4, 5, 6, 7),
        2: (2, 3, 4, 1, 5, 6, 7),
        3: (3, 4, 2, 1, 5, 6, 7),
        4: (4, 3, 2, 1, 5, 6, 7),
        5: (5, 6, 7, 2, 1, 3, 4),
        6: (6, 7, 5, 3, 2, 1, 4),
        7: (7, 6, 5, 4, 3, 1, 2)
    }

    return spawn_order.get(position, ())


#TODO are these the same across different effects (robin wood, helm of the gosling, juliets in graveyards)
# or do they behaave differently. Set up tests with tied attack and different cost, and tied attack&cost but different
# position and do so for both weaker and stronger style effects
def find_stat_extreme_character(player, strongest=True):
    # If there are no valid characters,  return nothing
    valid_characters = player.valid_characters()
    if not valid_characters:
        return None

    reverse = strongest
    sorted_chars = sorted(valid_characters, key=lambda char: (char.attack, char.cost, -1*char.position), reverse=reverse)
    return sorted_chars[0]


def find_strongest_character(player):
    return find_stat_extreme_character(player, strongest=True)


def find_weakest_character(player):
    return find_stat_extreme_character(player, strongest=False)

# DO NOT DO THIS
# TODO Summon random character with conditions
# DO NOT DO THIS
