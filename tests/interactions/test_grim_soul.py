import pytest

from sbbbattlesim import fight
from tests import make_character, make_player


@pytest.mark.parametrize('golden', (True, False))
def test_grimsoul(golden):
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_CERBERUS', position=1, attack=1, health=1, golden=golden),
            make_character(id='SBB_CHARACTER_NIGHTSTALKER', position=2, attack=1, health=1, golden=False),
            make_character(id='SBB_CHARACTER_RIVERWISHMERMAID', position=6, attack=1, health=1, golden=False),
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    enemy = make_player(
        characters=[make_character(attack=1, health=1)],
    )
    fight(player, enemy, limit=1)

    final_stats = (5, 5) if golden else (3, 3)
    assert (player.characters[2].attack, player.characters[2].health) == final_stats


def test_grimsoul_shouldnt_proc_lobo():
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_CERBERUS', position=1, attack=1, health=1),
            make_character(id='SBB_CHARACTER_SHADOWASSASSIN', position=2, attack=1, health=1, golden=False),
            make_character(id='SBB_CHARACTER_LOBO', position=6, attack=1, health=1, golden=False),
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    enemy = make_player(
        characters=[make_character(attack=1, health=1)],
    )
    fight(player, enemy, limit=1)

    assert (player.characters[2].attack, player.characters[2].health) == (1, 1)


def test_grimsoul_southsea():
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_CERBERUS', position=1, attack=1, health=1),
            make_character(id='SBB_CHARACTER_LOBO', position=2, attack=1, health=1, golden=False),
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    enemy = make_player(
        characters=[make_character(attack=1, health=1)],
    )
    fight(player, enemy, limit=1)


@pytest.mark.parametrize('golden', (True, False))
def test_grimsoul_listeners(golden):
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_CERBERUS', position=1, attack=1, health=1, golden=golden),
            make_character(id='SBB_CHARACTER_NIGHTSTALKER', position=2, attack=1, health=1, golden=False),
            make_character(id='SBB_CHARACTER_RIVERWISHMERMAID', position=6, attack=1, health=1, golden=False),
            make_character(id='SBB_CHARACTER_SHADOWASSASSIN', position=7, attack=1, health=1, holden=False)
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    enemy = make_player(
        characters=[make_character(attack=1, health=1)],
    )
    fight(player, enemy, limit=1)

    result = 3 if golden else 2
    assert player.characters[7].attack == result


@pytest.mark.parametrize('golden', (True, False))
def test_grimsoul_listeners_with_yaga(golden):
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_CERBERUS', position=1, attack=1, health=1, golden=golden),
            make_character(id='SBB_CHARACTER_NIGHTSTALKER', position=3, attack=1, health=1, golden=False),
            make_character(id='SBB_CHARACTER_SHADOWASSASSIN', position=5, attack=1, health=1, holden=False),
            make_character(id='SBB_CHARACTER_RIVERWISHMERMAID', position=6, attack=1, health=1, golden=False),
            make_character(id='SBB_CHARACTER_BABAYAGA', position=7, attack=1, health=1, golden=False),
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    enemy = make_player(
        characters=[make_character(attack=1, health=1)],
    )
    fight(player, enemy, limit=1)

    result = 5 if golden else 3
    assert player.characters[5].attack == result