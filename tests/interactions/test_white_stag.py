import pytest

from sbbbattlesim import fight
from tests import make_character, make_player


@pytest.mark.parametrize('golden', (True, False))
def test_stag(golden):
    player = make_player(
        characters=[
            make_character(id="SBB_CHARACTER_THEWHITESTAG", position=2, attack=1, health=1, golden=golden),
            make_character(position=5, attack=1, health=1),
            make_character(position=6, attack=1, health=1),
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    enemy = make_player(
        characters=[make_character(attack=0, health=100)],
    )
    fight(player, enemy, limit=1)


    final_stats = (7, 7) if golden else (4, 4)

    assert (player.characters[2].attack, player.characters[2].health) == (1, 1)
    for i in [5, 6]:
        assert (player.characters[i].attack, player.characters[i].health) == final_stats
