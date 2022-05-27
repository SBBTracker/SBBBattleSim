import pytest

from sbbbattlesim import fight
from sbbbattlesim.utils import Tribe
from tests import make_character, make_player


@pytest.mark.parametrize('golden', (True, False))
def test_angry(golden):
    player = make_player(
        raw=True,
        characters=[
            make_character(
                id="SBB_CHARACTER_DWARFMINER", position=1, attack=1, health=2,
                golden=golden, tribes=[Tribe.DWARF]
            ),
            make_character(position=6, attack=1, health=1, tribes=[Tribe.DWARF]),
        ],
    )
    enemy = make_player(
        raw=True,
        treasures=['''SBB_TREASURE_HERMES'BOOTS'''],
        characters=[
            make_character(position=1, attack=1, health=1),
            make_character(position=2, attack=3, health=3),
        ],

    )
    fight(player, enemy, limit=2)

    if golden:
        angry_final_stats = (9, 6)
        dorf_final_stats = (9, 9)
    else:
        dorf_final_stats = (3, 3)

    assert (player.characters[6].attack, player.characters[6].health) == dorf_final_stats
    if golden:
        assert (player.characters[1].attack, player.characters[1].health) == angry_final_stats
    else:
        assert player.characters[1] is None
