import pytest

from sbbbattlesim import fight
from tests import make_character, make_player


@pytest.mark.parametrize('golden', (True, False))
def test_sporko(golden):
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_MAGEMASTER', position=5, attack=3, health=6, golden=golden),
            make_character(position=2),
            make_character(position=1)
        ]
    )
    enemy = make_player()
    fight(player, enemy)


    char = player.characters[1]
    buffs = [
        r for r in char._action_history
    ]

    healthbuffs = sum([b.health for b in buffs])
    attackbuffs = sum([b.attack for b in buffs])

    assert attackbuffs == (8 if golden else 4)
    assert healthbuffs == 0

    char = player.characters[2]
    buffs = [
        r for r in char._action_history
    ]

    healthbuffs = sum([b.health for b in buffs])
    attackbuffs = sum([b.attack for b in buffs])

    assert attackbuffs == (8 if golden else 4)
    assert healthbuffs == 0



def test_sporko_ranged():
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_MAGEMASTER', position=6, attack=3, health=6),
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    enemy = make_player(
        characters=[make_character(attack=1, health=1)],
    )
    fight(player, enemy, limit=2)


    assert (player.characters[6].attack, player.characters[6].health) == (3, 6)
