import pytest

from sbbbattlesim import Board
from tests import make_character, make_player


@pytest.mark.parametrize('golden', (True, False))
def test_black_cat_dying(golden):

    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_BLACKCAT', position=6, golden=golden),
        ],
    )
    enemy = make_player(
        characters=[make_character(attack=500, health=500)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=1)
    board.p1.resolve_board()
    board.p2.resolve_board()

    final_stats = (2, 2) if golden else (1, 1)
    assert board.p1.characters[6].display_name == 'Cat'
    assert board.p1.characters[6].attack, board.p1.characters[6].health == final_stats
