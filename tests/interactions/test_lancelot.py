import pytest

from sbbbattlesim import fight
from tests import make_character, make_player


@pytest.mark.parametrize('golden', (True, False))
def test_lancelot(golden):
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_LANCELOT', position=6, attack=1, health=1, golden=golden),
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    enemy = make_player(
        characters=[make_character(attack=0, health=1)],
    )
    fight(player, enemy, limit=1)

    final_stats = (5, 5) if golden else (3, 3)
    assert (player.characters[6].attack, player.characters[6].health) == final_stats
