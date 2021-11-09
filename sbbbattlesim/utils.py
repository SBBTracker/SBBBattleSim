import enum
import random


LOKI_SPELLS = (
    '''SBB_SPELL_TESTYOURMIGHT''',  # Magic Research
    '''SBB_SPELL_SUGARANDSPICE''',  # Sugar and Spice
    '''SBB_SPELL_WITCHS'SBREW''',  # Witch's Brew
    '''SBB_SPELL_DRINKMEPOTION''',  # Luna's Grace
    '''SBB_SPELL_SAPMAGIC''',  # Flourish
    '''SBB_SPELL_MONSTERMASH''',  # Worm Root
    '''SBB_SPELL_BELLE'SINFLUENCE''',  # Beauty's Influence
    '''SBB_SPELL_FLAMINGAURA''',  # Burning Palm
    '''SBB_SPELL_STONESKIN''',  # Stoneskin
    '''SBB_SPELL_MERLIN'SHAT''',  # Merlin's Test
    '''SBB_SPELL_ROYALPOWER''',  # Queen's Grace
    '''SBB_SPELL_GIGANTIFY''',  # Gigantify
    '''SBB_SPELL_HUGEIFY''',  # Hugeify
    '''SBB_SPELL_KNIGHTHOOD''',  # Knighthood
    '''SBB_SPELL_TESTYOURMIGHT''',  # Evil Twin
)


class Tribe(enum.Enum):
    ANIMAL = 'animal'
    DRAGON = 'dragon'
    DWARF = 'dwarf'
    EGG = 'egg'
    FAIRY = 'fairy'
    MAGE = 'mage'
    MONSTER = 'monster'
    PRINCE = 'prince'
    PRINCESS = 'princess'
    PUFF_PUFF = 'puff puff'
    QUEEN = 'queen'
    TREANT = 'treant'

    GOOD = 'good'
    EVIL = 'evil'


class Keyword(enum.Enum):
    SUPPORT = 'support'
    FLYING = 'flying'
    SLAY = 'slay'
    LAST_BREATH = 'last breath'
    RANGED = 'ranged'
    QUEST = 'quest'


class StatChangeCause(enum.Enum):
    DAMAGE_WHILE_ATTACKING = 1
    DAMAGE_WHILE_DEFENDING = 2
    SUPPORT_BUFF = 3
    AURA_BUFF = 4
    SLAY = 5

    ANGRY_BUFF = 101
    DOUBLEY_BUFF = 102
    FRIENDLY_SPIRIT_BUFF = 103
    PUFF_PUFF_BUFF = 107
    ROBIN_WOOD_DEBUFF = 108
    ROBIN_WOOD_BUFF = 109
    ROTTEN_APPLE_TREE_HEALTH = 110
    SHOULDER_FAIRY_BUFF = 111
    WRETCHED_MUMMY_EXPLOSION = 120

    BLESSING_OF_ATHENA = 401
    LUNAS_GRAVE = 402
    RIDE_OF_THE_VALKYRIES = 403
    SUGAR_AND_SPICE = 404
    MAGIC_RESEARCH = 405
    WITCHS_BREW = 406
    GIGANTIFY = 407
    HUGEIFY = 408
    STONE_SKIN = 409
    WORM_ROOT = 410
    BEAUTYS_INFLUENCE = 411
    MERLINS_TEST = 412
    QUEENS_GRACE = 413

    SMITE = 450
    EARTHQUAKE = 451
    SHRIVEL = 452
    FALLING_STARS = 453
    FIREBALL = 454
    LIGHTNING_BOLT = 455
    POISON_APPLE = 456


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
# or do they behaave differently. Set up resources with tied attack and different cost, and tied attack&cost but different
# position and do so for both weaker and stronger style effects
def find_stat_extreme_character(player, strongest=True):
    # If there are no valid characters,  return nothing
    valid_characters = player.valid_characters()
    if not valid_characters:
        return None

    func = max if strongest else min
    sub_char = func(valid_characters, key=lambda char: (char.attack, char.cost))
    sub_chars = list(filter(lambda char: char.attack == sub_char.attack and char.cost == sub_char.cost, valid_characters))
    return random.choice(sub_chars)


def find_strongest_character(player):
    return find_stat_extreme_character(player, strongest=True)


def find_weakest_character(player):
    return find_stat_extreme_character(player, strongest=False)


# DO NOT DO THIS
# TODO Summon random character with conditions
# DO NOT DO THIS
