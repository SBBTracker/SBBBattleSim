from sbbbattlesim.characters import registry as character_registry


def make_player(characters, hero='', spell='', treasures=[], hand=[]):
    PLAYER = {
        'characters': characters,
        'treasures': treasures,
        'hero': hero,
        'spell': spell,
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


def make_monstar():
    return make_character(id='SBB_CHARACTER_MONSTAR', attack=50, health=50)


def get_characters(_lambda=lambda char: True):
    return [char for char in character_registry.characters.keys() if _lambda(char)]
