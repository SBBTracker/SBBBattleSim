import pytest

from sbbbattlesim import fight
from sbbbattlesim.utils import Tribe
from tests import make_character, make_player


@pytest.mark.parametrize('golden', (True, False))
def test_lordy(golden):
    player = make_player(
        characters=[
            make_character(
                id="SBB_CHARACTER_FORGEMASTERDWARF", position=1, attack=1, health=1, tribes=[Tribe.DWARF], golden=golden
            ),
            make_character(position=6, attack=1, health=1, tribes=[Tribe.DWARF]),
            make_character(position=5, attack=1, health=1),
        ],
    )
    enemy = make_player()

    fight(player, enemy, limit=0)



    if golden:
        final_stats = (9, 9)
    else:
        final_stats = (5, 5)

    d1stats = (player.characters[1].attack, player.characters[1].health)
    d6stats = (player.characters[6].attack, player.characters[6].health)
    not_d5stats = (player.characters[5].attack, player.characters[5].health)

    assert d1stats == final_stats
    assert d6stats == final_stats
    assert not_d5stats == (1, 1)
