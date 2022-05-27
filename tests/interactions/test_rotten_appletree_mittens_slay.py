import pytest

from sbbbattlesim import fight
from tests import make_character, make_player


@pytest.mark.parametrize('mittens', (True, False))
def test_rottenappletree_slay_mittens(mittens):

    player = make_player(
        characters=[
            make_character(id="SBB_CHARACTER_WORLDSERPENT", position=7, attack=40, health=40),
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    enemy = make_player(
        characters=[
            make_character(id="SBB_CHARACTER_ROTTENAPPLETREE", attack=0, health=1),
        ],
        treasures=[
            '''SBB_TREASURE_EXPLODINGMITTENS''' if mittens else ''
        ]
    )
    jorm = player.characters[7]
    fight(player, enemy, limit=1)

    assert not jorm.dead, jorm.pretty_print()
