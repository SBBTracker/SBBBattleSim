from sbbbattlesim import Board
from tests import make_player, make_character
import pytest


def test_support_none():
    board = Board({
        'Player': make_player(
            raw=True,
            characters=[
                make_character(id='SBB_CHARACTER_BLACKCAT', position=1),
                make_character(position=5)
            ]
        ),
        'Enemy': make_player(
            raw=True,
            characters=[
                make_character()
            ]
        )
    })


@pytest.mark.parametrize('r', range(30))
def test_invalid_state(r):
    board = Board({
        'Player': make_player(
            raw=True,
            characters=[
                make_character(attack=1, health=0),
            ]
        ),
        'Enemy': make_player(
            raw=True,
            characters=[
                make_character()
            ]
        )
    })

    winner, loser = board.fight(limit=100)
    #assert winner is board.p2
    #assert loser is board.p1


    assert board.p1.characters[1].attack == 1
    assert board.p1.characters[1].health == 0
    assert board.p2.characters[1].attack == 1
    assert board.p2.characters[1].health == 1




