import pytest

from sbbbattlesim import Board
from tests import make_character, make_player


@pytest.mark.parametrize('golden', (True, False))
def test_green_knight(golden):
    player = make_player(
        characters=[
            make_character(id="SBB_CHARACTER_THEGREENKNIGHT",position=5, attack=1, health=1, golden=golden),
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
        final_stats = (1, 21)
    else:
        final_stats = (1, 11)

    assert (board.p1.characters[1].attack, board.p1.characters[1].health) == final_stats