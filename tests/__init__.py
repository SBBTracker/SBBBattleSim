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
