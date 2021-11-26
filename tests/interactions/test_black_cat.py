from sbbbattlesim import Board
from tests import make_character, make_player
import pytest

def test_black_cat_dying():

    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_BLACKCAT', position=6),
        ],
    )
    enemy = make_player(
        characters=[make_character(attack=500, health=500)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=1)
    board.p1.resolve_board()
    board.p2.resolve_board()


    assert board.p1.characters[6].display_name == 'Cat'
