import pytest

from sbbbattlesim import Board
from sbbbattlesim.utils import Tribe
from tests import make_character, make_player


@pytest.mark.parametrize('golden', (True, False))
def test_shoulderfaeries(golden):
    player = make_player(
        characters=[
            make_character(
                id="SBB_CHARACTER_GOODANDEVILSISTERS", position=1, attack=1, health=1, golden=golden
            ),
            make_character(position=6, attack=1000, health=100, tribes=[Tribe.GOOD]),
            make_character(position=5, attack=100, health=1000, tribes=[Tribe.EVIL]),
        ],
    )
    enemy = make_player()

    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=0)
    board.p1.resolve_board()
    board.p2.resolve_board()

    if golden:
        final_stats = (201, 201)
    else:
        final_stats = (101, 101)

    assert (board.p1.characters[1].attack, board.p1.characters[1].health) == final_stats

# TODO figure out exactly how they work with round table
