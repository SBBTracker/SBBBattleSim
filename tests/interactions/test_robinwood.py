import pytest

from sbbbattlesim import fight
from sbbbattlesim.utils import Tribe
from tests import make_character, make_player


@pytest.mark.parametrize('golden', (True, False))
def test_robinwood(golden):
    player = make_player(
        characters=[
            make_character(
                id="SBB_CHARACTER_ROBINWOOD", position=5,
                attack=5, health=1, golden=golden, tribes=[Tribe.TREANT]
            ),
            make_character(position=2, attack=2, health=1),
        ],
    )
    enemy = make_player(
        characters=[
            make_character(position=1, attack=20),
            make_character(position=2, attack=5)
        ]
    )
    fight(player, enemy, limit=0)

    buffed_attack = (16 if golden else 9)

    assert (player.characters[2].attack, player.characters[2].health) == (buffed_attack, 1)
    assert (player.characters[5].attack, player.characters[5].health) == (5, 1)

    assert enemy.characters[1].attack == (6 if golden else 13)
    assert enemy.characters[2].attack == 5


def test_robinwood_ranged():
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_ROBINWOOD', position=6, attack=3, health=6),
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    enemy = make_player(
        characters=[make_character(attack=1, health=1)],
    )
    fight(player, enemy, limit=2)

    assert (player.characters[6].attack, player.characters[6].health) == (10, 6)
