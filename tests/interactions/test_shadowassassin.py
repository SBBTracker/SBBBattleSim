import pytest

from sbbbattlesim import fight
from tests import make_character, make_player


@pytest.mark.parametrize('golden', (True, False))
def test_shadow_assassin(golden):
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_LANCELOT', position=6, attack=1, health=1),
            make_character(id='SBB_CHARACTER_SHADOWASSASSIN', position=7, attack=1, health=1, golden=golden)
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    enemy = make_player(
        characters=[make_character(attack=0, health=1)],
    )
    fight(player, enemy, limit=1)


    final_stats = (3, 1) if golden else (2, 1)
    assert (player.characters[7].attack, player.characters[7].health) == final_stats
