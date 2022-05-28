import pytest

from sbbbattlesim import fight
from tests import make_character, make_player


@pytest.mark.parametrize('golden', (True, False))
def test_unassumingsheep(golden):
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_UNASSUMINGSHEEP', position=6, golden=golden),
        ],
    )
    enemy = make_player(
        characters=[make_character(attack=500, health=500)],
    )
    fight(player, enemy, limit=1)


    final_stats = (12, 12) if golden else (6, 6)
    assert player.characters[6].id == 'SBB_CHARACTER_EVILWOLF', player.characters[6].pretty_print()
    assert player.characters[6].attack, player.characters.health == final_stats
