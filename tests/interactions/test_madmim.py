from sbbbattlesim import Board
from tests import make_character, make_player
from sbbbattlesim.utils import Tribe
import pytest

@pytest.mark.parametrize('golden', (True, False))
def test_madmim(golden):
    player = make_player(
        characters=[
            make_character(id="SBB_CHARACTER_MADMADAMMIM",position=5, attack=1, health=1, golden=golden),
            make_character(position=1, attack=1, health=1),
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    enemy = make_player()
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=2)
    board.p1.resolve_board()
    board.p2.resolve_board()

    if golden:
        final_stats = (7, 1)
    else:
        final_stats = (4, 1)

    assert (board.p1.characters[1].attack, board.p1.characters[1].health) == final_stats