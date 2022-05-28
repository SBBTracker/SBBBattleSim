import pytest

from sbbbattlesim import fight
from tests import make_character, make_player


@pytest.mark.parametrize('golden', (True, False))
def test_black_cat_dying(golden):
    player = make_player(
        raw=True,
        characters=[
            make_character(id='SBB_CHARACTER_BLACKCAT', position=6, golden=golden),
        ],
    )
    enemy = make_player(
        raw=True,
        characters=[make_character(attack=500, health=500)],
    )
    fight(player, enemy, limit=1)

    final_stats = (2, 2) if golden else (1, 1)
    assert player.characters[6].display_name == 'Cat'
    assert player.characters[6].attack, player.characters[6].health == final_stats
