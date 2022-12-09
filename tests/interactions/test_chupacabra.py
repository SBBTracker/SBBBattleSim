import pytest
from sbbbattlesim.utils import Tribe

from sbbbattlesim import fight
from tests import make_character, make_player


@pytest.mark.parametrize('golden', (True, False))
def test_chup(golden):
    player = make_player(
        raw=True,
        characters=[
            make_character(id="SBB_CHARACTER_THECHUPACABRA", position=2, attack=1, health=1, golden=golden, tribes=[Tribe.MONSTER]),
            make_character(position=5, attack=1, health=1, tribes=[Tribe.MONSTER]),
            make_character(position=3, attack=1, health=1, tribes=[Tribe.MONSTER]),
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    enemy = make_player(
        raw=True,
        characters=[make_character(attack=0, health=1)],
    )
    fight(player, enemy, limit=1)

    final_stats = (3, 1) if golden else (2, 1)

    for i in [2, 5, 3]:
        assert (player.characters[i].attack, player.characters[i].health) == final_stats
