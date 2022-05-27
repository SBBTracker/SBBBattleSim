import pytest

from sbbbattlesim import fight
from tests import make_character, make_player


@pytest.mark.skipif
@pytest.mark.parametrize('golden', (True, False))
@pytest.mark.parametrize('mimic', (True, False))
@pytest.mark.parametrize('evil_eye', (True, False))
def test_riverwish_yaga(golden, mimic, evil_eye):
    player = make_player(
        raw=True,
        characters=[
            make_character(id='SBB_CHARACTER_RIVERWISHMERMAID', position=5, attack=5, health=5, golden=False),
            make_character(id='SBB_CHARACTER_BABAYAGA', position=6, attack=3, health=6, golden=golden),
            make_character(position=2),
            make_character(id="SBB_CHARACTER_SHADOWASSASSIN", position=7, attack= 1, health=1)
        ],
        treasures=[
            'SBB_TREASURE_HELMOFCOMMAND' if evil_eye else '',
            'SBB_TREASURE_TREASURECHEST' if mimic else '',
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    enemy = make_player(
        raw=True,
        characters=[make_character(attack=0, health=1)],
    )
    fight(player, enemy, limit=1)

    yaga_multiplier = 2 if golden else 1
    evil_eye_additor = yaga_multiplier if evil_eye else 0
    mimic_multiplier = 2 if mimic else 1

    slay_multiplyer = 1 + yaga_multiplier + evil_eye_additor * mimic_multiplier
    slay_count = 1
    if mimic and evil_eye:
        slay_count = 3
    elif evil_eye:
        slay_count = 2

    final_stat = 1 + slay_count * slay_multiplyer
    final_stats = (final_stat, final_stat)

    assert (player.characters[2].attack, player.characters[2].health) == final_stats
    assert (player.characters[7].attack, player.characters[7].health) == (final_stat, 1)


@pytest.mark.parametrize('mimic', (True, False))
@pytest.mark.parametrize('evil_eye', (True, False))
def test_double_yaga(mimic, evil_eye):
    player = make_player(
        raw=True,
        characters=[
            make_character(id='SBB_CHARACTER_BABAYAGA', position=5, attack=5, health=5, golden=False),
            make_character(id='SBB_CHARACTER_BABAYAGA', position=6, attack=3, health=6, golden=False),
            make_character(id='SBB_CHARACTER_CATBURGLAR', position=2, attack=1, health=1),
            make_character(id="SBB_CHARACTER_SHADOWASSASSIN", position=7, attack=1, health=1)
        ],
        treasures=[
            'SBB_TREASURE_HELMOFCOMMAND' if evil_eye else '',
            'SBB_TREASURE_TREASURECHEST' if mimic else '',
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    enemy = make_player(
        raw=True,
        characters=[make_character(attack=0, health=1)],
    )
    fight(player, enemy, limit=1)

    evil_eye_additor = 1 if evil_eye else 0
    mimic_multiplier = 2 if mimic else 1

    slay_multiplyer = 1 + evil_eye_additor * mimic_multiplier
    slay_count = 1

    final_stat = 1 + 1 + slay_count * slay_multiplyer * 2
    final_stats = (final_stat, final_stat)

    assert (player.characters[7].attack, player.characters[7].health) == (final_stat, 1)


def test_complicated_grimsoul():
    player = make_player(
        raw=True,
        hero="SBB_HERO_MILITARYLEADER",
        characters=[
            make_character(id='SBB_CHARACTER_BABAYAGA', position=5, attack=5, health=5, golden=False),
            make_character(id='SBB_CHARACTER_RIVERWISHMERMAID', position=6, attack=5, health=5, golden=False),
            make_character(id='SBB_CHARACTER_CERBERUS', position=2, attack=10, health=10, golden=False)
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    enemy = make_player(
        raw=True,
        characters=[make_character(attack=0, health=1)],
    )
    fight(player, enemy, limit=1)

    assert (player.characters[2].attack, player.characters[2].health) == (12, 12)


def test_complicated_grimsoul_two():
    player = make_player(
        raw=True,
        hero="SBB_HERO_MILITARYLEADER",
        characters=[
            make_character(id='SBB_CHARACTER_CERBERUS', position=3, attack=10, health=10, golden=False),
            make_character(id='SBB_CHARACTER_RIVERWISHMERMAID', position=6, attack=5, health=5, golden=False),
            make_character(id='SBB_CHARACTER_CERBERUS', position=2, attack=10, health=10, golden=False)
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    enemy = make_player(
        raw=True,
        characters=[make_character(attack=0, health=1)],
    )
    fight(player, enemy, limit=1)

    leftgrim = player.characters[2]
    rightgrim = player.characters[3]
    assert rightgrim.attack + leftgrim.attack == 21
    assert rightgrim.health + leftgrim.health == 21


def test_trophy_grimsoul_blackcat():
    player = make_player(
        raw=True,
        hero="SBB_HERO_MILITARYLEADER",
        characters=[
            make_character(id='SBB_CHARACTER_BABAYAGA', position=5, attack=5, health=5, golden=False),
            make_character(id='SBB_CHARACTER_BLACKCAT', position=2, attack=5, health=5, golden=False),
            make_character(id='SBB_CHARACTER_CERBERUS', position=1, attack=10, health=10, golden=False)
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    enemy = make_player(
        characters=[make_character(attack=0, health=1)],
    )
    fight(player, enemy, limit=1)

    assert player.characters[3].id == "SBB_CHARACTER_CAT"
    assert player.characters[4].id == "SBB_CHARACTER_CAT"
    assert player.characters[6].id == "SBB_CHARACTER_CAT"
    assert player.characters[7].id == "SBB_CHARACTER_CAT"




