import pytest

from sbbbattlesim import fight
from tests import make_character, make_player


@pytest.mark.skipif
@pytest.mark.parametrize('golden', (True, False))
def test_broc_lee(golden):
    player = make_player(
        raw=True,
        characters=[
            make_character(id="SBB_CHARACTER_RAZORLEAFOAK", position=1, attack=0, health=100, golden=golden),
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    enemy = make_player(
        raw=True,
        characters=[
            make_character(attack=1, health=1, position=1),
            make_character(attack=1, health=1, position=2)
        ],
    )
    fight(player, enemy, limit=-1)

    assert player.characters[1].attack == (60 if golden else 30)
