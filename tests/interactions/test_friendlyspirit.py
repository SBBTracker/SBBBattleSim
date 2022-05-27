import pytest

from sbbbattlesim import fight
from tests import make_character, make_player


@pytest.mark.parametrize('golden', (True, False))
def test_friendlyspirit(golden):
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_FRIENDLYGHOST', position=1, attack=5, health=5, golden=golden),
            make_character(position=7)
        ],
    )
    enemy = make_player(
        characters=[
            make_character(attack=5, health=5),
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    fight(player, enemy, limit=1)

    assert (player.characters[7].attack, player.characters[7].health) == (11, 11) if golden else (6, 6)
