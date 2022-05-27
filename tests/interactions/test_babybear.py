import pytest

from sbbbattlesim import fight
from tests import make_character, make_player


@pytest.mark.parametrize('golden', (True, False))
@pytest.mark.parametrize('limit', (1, 2))
def test_babybear_dying(golden, limit):
    player = make_player(
        raw=True,
        characters=[
            make_character(id='SBB_CHARACTER_BABYBEAR', position=6,
                           attack=2 if golden else 1, health=2 if golden else 1, golden=golden),
        ],
    )
    enemy = make_player(
        raw=True,
        characters=[make_character(attack=500, health=500)],
    )
    fight(player, enemy, limit=limit)

    if limit == 1:
        assert player.characters[6].id == 'SBB_CHARACTER_PAPABEAR'
    if limit == 2:
        assert player.characters[6].id == 'SBB_CHARACTER_MAMABEAR'
