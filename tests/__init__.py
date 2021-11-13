from sbbbattlesim.characters import registry as character_registry
from sbbbattlesim.spells import registry as spell_registry
from sbbbattlesim.treasures import registry as treasure_registry

PLAYER = {
    'characters': [],
    'treasures': [],
    'hero': '',
    'spells': [],
    'hand': [],
    'level': 0
}

CHARACTER = {
    "id": 'TEST',
    "attack": 1,
    "health": 1,
    "golden": False,
    "cost": 0,
    "level": 0,
    "position": 1,
    "keywords": [],
    "tribes": []
}


def make_player(**kwargs):
    player = PLAYER.copy()
    player.update(kwargs)
    return player


def make_character(**kwargs):
    character = CHARACTER.copy()
    character.update(kwargs)
    return character


def get_characters(_lambda=lambda char: True):
    return [key for key, char in character_registry.characters.items() if _lambda(char)]


def get_spells(_lambda=lambda spell: True):
    return [key for key, spell in spell_registry.spells.items() if _lambda(spell)]


def get_treasures(_lambda=lambda treasure: True):
    return [key for key, treasure in treasure_registry.treasures.items() if _lambda(treasure)]
