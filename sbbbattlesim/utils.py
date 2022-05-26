import enum
import logging
import random
from functools import cache

logger = logging.getLogger(__name__)

from sbbbattlesim.spells import registry as spell_registry

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
# combat spells could be used and shared between deck, book of merlin and monster book
COMBAT_SPELLS = (
    '''SBB_SPELL_FALLINGSTARS''',
    '''SBB_SPELL_EARTHQUAKE''',
    '''SBB_SPELL_RIDEOFTHEVALKYRIES''',
    '''SBB_SPELL_ANGEL'SBLESSING''',
    '''SBB_SPELL_LIGHTNINGBOLT''',
    '''SBB_SPELL_FIREBALL''',
    '''SBB_SPELL_ENFEEBLEMENT''',
    '''SBB_SPELL_POISONAPPLE''',
    '''SBB_SPELL_DISINTEGRATE''',
    '''SBB_SPELL_PIGOMORPH''',
)

START_OF_FIGHT_SPELLS = (
    '''SBB_SPELL_FALLINGSTARS''',
    '''SBB_SPELL_EARTHQUAKE''',
    '''SBB_SPELL_RIDEOFTHEVALKYRIES''',
    '''SBB_SPELL_ANGEL'SBLESSING''',
    '''SBB_SPELL_LIGHTNINGBOLT''',
    '''SBB_SPELL_FIREBALL''',
    '''SBB_SPELL_ENFEEBLEMENT''',
    '''SBB_SPELL_POISONAPPLE''',
    '''SBB_SPELL_DISINTEGRATE''',
    '''SBB_SPELL_PIGOMORPH''',
    '''SBB_SPELL_BEASTWITHIN''',
    '''SBB_SPELL_MENAGERIE''',
    '''SBB_SPELL_FOG'''
)


class Tribe(enum.Enum):
    ANIMAL = 'animal'
    DRAGON = 'dragon'
    DWARF = 'dwarf'
    EGG = 'egg'
    FAIRY = 'fairy'
    MAGE = 'mage'
    MONSTER = 'monster'
    ROYAL = 'royal'
    PUFF_PUFF = 'puff'
    QUEEN = 'queen'
    TREANT = 'treant'

    GOOD = 'good'
    EVIL = 'evil'

@cache
def get_adjacent_targets(position):
    return {
        1: (2,),
        2: (1, 3),
        3: (2, 4),
        4: (3,),
        5: (6,),
        6: (5, 7),
        7: (7,)
    }.get(position, ())


@cache
def get_support_targets(position, horn=False):
    if horn:
        return [1, 2, 3, 4]
    return {
        5: (1, 2),
        6: (2, 3),
        7: (3, 4)
    }.get(position, ())


@cache
def get_behind_targets(position):
    return {
        1: (5,),
        2: (5, 6),
        3: (6, 7),
        4: (7,)
    }.get(position, ())


@cache
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


def random_combat_spell(level):
    valid_spells = list(spell_registry.filter(_lambda=lambda spell_cls: (spell_cls._level <= level or spell_cls._level == 3) and spell_cls.id in COMBAT_SPELLS))
    if valid_spells:
        return random.choice(valid_spells)


def random_start_combat_spell(level):
    valid_spells = list(spell_registry.filter(_lambda=lambda spell_cls: (spell_cls._level <= level or spell_cls._level == 3) and spell_cls.id in START_OF_FIGHT_SPELLS))
    if valid_spells:
        return random.choice(valid_spells)


# TODO are these the same across different effects (robin wood, helm of the gosling, juliets in graveyards)
# or do they behaave differently. Set up resources with tied attack and different cost, and tied attack&cost but different
# position and do so for both weaker and stronger style effects
def find_stat_extreme_character(player, strongest=True):
    # If there are no valid characters,  return nothing
    valid_characters = player.valid_characters()
    if not valid_characters:
        return None

    func = max if strongest else min
    sub_char = func(valid_characters, key=lambda char: (char.attack, char.cost, char.position))
    sub_chars = list(
        filter(lambda char: char.attack == sub_char.attack and char.cost == sub_char.cost, valid_characters))
    return random.choice(sub_chars)


def find_strongest_character(player):
    return find_stat_extreme_character(player, strongest=True)


def find_weakest_character(player):
    return find_stat_extreme_character(player, strongest=False)

# DO NOT DO THIS
# TODO Summon random character with conditions
# DO NOT DO THIS
