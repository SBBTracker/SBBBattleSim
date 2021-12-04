from sbbbattlesim import Board
from tests import make_character, make_player
import pytest

def test_robinwood_doubly():

    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_DUMBLEDWARF', position=5, attack=31, health=1),
        ],
    )
    enemy = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_ROBINWOOD', attack=1, health=1),
        ],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=0)
    board.p1.resolve_board()
    board.p2.resolve_board()


    assert (board.p1.characters[5].attack, board.p1.characters[5].health) == (1, 1)