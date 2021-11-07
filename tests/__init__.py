import json

from sbbbattlesim import Board


def make_fight(player, enemy):
    return Board({'PLAYER': player, 'ENEMY': enemy})


def make_player(characters, hero='', spell='', treasures=[], hand=[]):
    PLAYER = {
        'characters': characters,
        'treasures': treasures,
        'hero': hero,
        'spell': spell,
        'hand': hand,
    }

    return PLAYER


def make_character(id, position=None, attack=0, health=1, golden=False, cost=0, level=0, keywords=[], tribes=[]):
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


def fight_monstar(player):
    monstar = make_player([make_character(id='SBB_CHARACTER_MONSTAR', attack=50, health=50)])
    return make_fight(player, monstar)