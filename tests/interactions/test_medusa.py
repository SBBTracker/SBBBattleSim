import pytest

from sbbbattlesim import fight
from tests import make_character, make_player


@pytest.mark.parametrize('golden', (True, False))
def test_medusa(golden):
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_MEDUSA', position=6, attack=1, health=1, golden=golden),
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    enemy = make_player(
        characters=[make_character(attack=1, health=1)],
    )
    creature = enemy.characters[1]
    fight(player, enemy, limit=3)
    statue = enemy.characters[1]



    assert creature is not statue
    assert statue.health == (1 if golden else 4)


@pytest.mark.parametrize('defending_pos', (1, 2, 3, 4))
def test_medusa_attackslot(defending_pos):
    '''Test that dusa attacking the first unit doesnt break the attack order, and still allows the first attack slot to attack'''
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_MEDUSA', attack=1, health=5, position=6),
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    enemy = make_player(
        characters=[
            make_character(attack=1, health=1, position=defending_pos),
            make_character(attack=10, health=1, position=5)
        ],
        treasures=[
            '''SBB_TREASURE_POWERGEM'''
        ]
    )
    fight(player, enemy, limit=2)



    dusa = player.characters[6]
    assert dusa
    assert dusa.health == 3


@pytest.mark.parametrize('attacking_pos', (1, 2, 3, 4))
def test_medusa_attackslot_2(attacking_pos):
    '''Test that if the first attack slot attacks and then dusa attacks it back, that the statue will not attack back again'''
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_MEDUSA', position=6, attack=1, health=5),
        ],
        treasures=[
        ]
    )
    enemy = make_player(
        characters=[
            make_character(attack=1, health=10, position=attacking_pos),
            make_character(attack=10, health=1, position=5)
        ],
        treasures=[
            '''SBB_TREASURE_POWERGEM''',
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    dusa = player.characters[6]

    fight(player, enemy, limit=3)



    assert dusa
    assert dusa.dead


def test_medusa_cupid():
    player = make_player(
        characters=[
            make_character(position=4, attack=1, health=1),
            make_character(id='SBB_CHARACTER_MEDUSA', position=6, attack=1, health=5),
        ]
    )
    enemy = make_player(
        characters=[make_character(id="SBB_CHARACTER_CUPID", attack=1, health=1)],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    creature = player.characters[4]
    fight(player, enemy, limit=1)
    statue = player.characters[4]



    assert creature is not statue
    assert statue.health == 5
