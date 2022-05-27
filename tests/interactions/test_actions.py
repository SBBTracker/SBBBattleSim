import pytest

from sbbbattlesim import fight
from tests import make_player, make_character


def test_support_none():
    make_player(
        raw=True,
        characters=[
            make_character(id='SBB_CHARACTER_BLACKCAT', position=1),
            make_character(position=5)
        ]
    )


@pytest.mark.parametrize('r', range(30))
def test_invalid_state(r):
    player = make_player(
        raw=True,
        characters=[
            make_character(attack=1, health=0),
        ]
    )
    enemy = make_player(
        raw=True,
        characters=[
            make_character()
        ]
    )

    fight(player, enemy, limit=100)
    #assert winner is enemy
    #assert loser is player

    assert player.characters[1].attack == 1
    assert player.characters[1].health == 0
    assert enemy.characters[1].attack == 1
    assert enemy.characters[1].health == 1




