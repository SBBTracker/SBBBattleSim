import pytest

from sbbbattlesim import fight
from tests import make_character, make_player


@pytest.mark.parametrize('golden', (True, False))
def test_mummy(golden):
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_WRETCHEDMUMMY', position=1, attack=5, health=1, golden=golden),
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    enemy = make_player(
        characters=[
            make_character(attack=1, health=1, position=1),
            make_character(attack=0, health=100, position=5)
        ],
    )
    fight(player, enemy, limit=1)


    assert enemy.characters[5].health == 90 if golden else 95
