from sbbbattlesim.characters import registry as character_registry
from sbbbattlesim.spells import registry as spell_registry
from sbbbattlesim.treasures import registry as treasure_registry


def make_player(characters, hero='', spells=[], treasures=[], hand=[]):
    PLAYER = {
        'characters': characters,
        'treasures': treasures,
        'hero': hero,
        'spells': spells,
        'hand': hand,
    }

    return PLAYER


def make_character(id, position, attack=1, health=1, golden=False, cost=0, level=0, keywords=[], tribes=[]):
    CHARACTER = {
        "id": id,
        "attack": attack,
        "health": health,
        "golden": golden,
        "cost": cost,
        "level": level,
        "position": position,
        "keywords": keywords,
        "tribes": tribes
    }

    return CHARACTER


def get_characters(_lambda=lambda char: True):
    return [key for key, char in character_registry.characters.items() if _lambda(char)]


def get_spells(_lambda=lambda spell: True):
    return [key for key, spell in spell_registry.spells.items() if _lambda(spell)]


def get_treasures(_lambda=lambda treasure: True):
    return [key for key, treasure in treasure_registry.treasures.items() if _lambda(treasure)]
