import pytest

from sbbbattlesim import fight
from sbbbattlesim.utils import Tribe
from tests import make_character, make_player


@pytest.mark.parametrize('golden', (True, False))
def test_queenofhearts(golden):
    player = make_player(
        raw=True,
        hero="SBB_HERO_MUERTE",
        characters=[
            make_character(id="SBB_CHARACTER_BLACKCAT", position=2, attack=1, health=1, tribes=[Tribe.EVIL]),
            make_character(position=1, attack=1, health=1),
            make_character(id="SBB_CHARACTER_QUEENOFHEARTS", position=6, attack=1, health=1, golden=golden),
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    enemy = make_player(
        raw=True,
        characters=[
            make_character(health=3)
        ],
    )
    fight(player, enemy, limit=3)

    if golden:
        final_stats = (9, 9)
    else:
        final_stats = (5, 5)

    assert (player.characters[6].attack, player.characters[6].health) == final_stats
