import pytest

from sbbbattlesim import fight
from tests import make_character, make_player


@pytest.mark.parametrize('golden', (True, False))
def test_threebigpigs(golden):
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_THREEBIGPIGS', position=1, golden=golden),
        ],
    )
    enemy = make_player(
        characters=[make_character(attack=500, health=500)],
    )
    fight(player, enemy, limit=1)


    final_stats = (2, 2) if golden else (1, 1)
    for i in [1, 2, 3]:
        assert player.characters[i].id == 'SBB_CHARACTER_PIGGY', player.characters[i].pretty_print()
        assert player.characters[i].attack, enemy.characters[i].health == final_stats
