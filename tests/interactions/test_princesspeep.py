from sbbbattlesim import Board
from tests import make_character, make_player
import pytest

def test_peep_dying():

    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_PRINCESSPEEP', position=1),
        ],
    )
    enemy = make_player(
        characters=[make_character(attack=500, health=500)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=1)
    board.p1.resolve_board()
    board.p2.resolve_board()


    assert board.p1.characters[1].display_name == 'Sheep'
    assert board.p1.characters[2].display_name == 'Sheep'
    assert board.p1.characters[3].display_name == 'Sheep'
