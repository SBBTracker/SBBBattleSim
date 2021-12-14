from sbbbattlesim import Board
from tests import make_player, make_character


def test_support_none():
    board = Board({
        'Player': make_player(
            characters=[
                make_character(id='SBB_CHARACTER_BLACKCAT', position=1),
                make_character(position=5)
            ]
        ),
        'Enemy': make_player(
            characters=[
                make_character()
            ]
        )
    })