from sbbbattlesim import Board
from tests import make_character, make_player
import pytest

def test_rotten_appletree():

    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_ROTTENAPPLETREE', position=6, attack=0, health=5),
        ]
    )
    enemy = make_player(
        characters=[
            make_character(attack=1, health=1000, position=1),
        ]
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=2)
    board.p1.resolve_board()
    board.p2.resolve_board()

    assert board.p2.characters[1].health == 1

