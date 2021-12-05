import pytest

from sbbbattlesim import Board
from sbbbattlesim.utils import Tribe
from tests import make_character, make_player



def test_egg_feather():
    player = make_player(
        treasures=['''SBB_TREASURE_PHOENIXFEATHER'''],
        characters=[
            make_character(
                id="SBB_CHARACTER_HUMPTYDUMPTY",position=1, attack=1, health=1,
                golden=False
            ),
        ],
    )
    enemy = make_player(

        characters = [
            make_character(position=1, attack=1, health=1),
         ],

    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=2)
    board.p1.resolve_board()
    board.p2.resolve_board()


    assert board.p1.characters[1] is None
