import pytest

from sbbbattlesim import fight
from tests import make_character, make_player


@pytest.mark.parametrize('golden', (True, False))
@pytest.mark.parametrize('on', (True, False))
def test_wraith(golden, on):
    p = 2 if on else 3
    player = make_player(
        characters=[
            make_character(id="SBB_CHARACTER_WATERWRAITH", position=p, attack=1, health=1, golden=golden),
            make_character(position=1, attack=1, health=1),
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    enemy = make_player(
        characters=[make_character(attack=500, health=500)]
    )
    fight(player, enemy, limit=1)

    if not on:
        final_stats = (1, 1)
    elif golden:
        final_stats = (3, 3)
    else:
        final_stats = (2, 2)

    assert (player.characters[p].attack, player.characters[p].health) == final_stats


