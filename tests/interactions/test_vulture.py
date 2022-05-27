import pytest

from sbbbattlesim import fight
from sbbbattlesim.utils import Tribe
from tests import make_character, make_player


@pytest.mark.parametrize('golden', (True, False))
def test_vulture(golden):
    player = make_player(
        characters=[
            make_character(
                id="SBB_CHARACTER_VULTURE", position=5, golden=golden,
                attack=1, health=1, tribes=[Tribe.ANIMAL]
            ),
            make_character(position=1, attack=1, health=1, tribes=[Tribe.ANIMAL]),
            make_character(position=2, attack=1, health=1),
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    enemy = make_player(
        characters=[
            make_character(health=2)
        ],
    )
    fight(player, enemy, limit=2)


    if golden:
        final_stats = (7, 7)
    else:
        final_stats = (4, 4)

    assert (player.characters[5].attack, player.characters[5].health) == final_stats
