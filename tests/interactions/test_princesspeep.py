from sbbbattlesim import Board
from tests import make_character, make_player
import pytest

@pytest.mark.parametrize('golden', (True, False))
def test_peep_dying(golden):

    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_PRINCESSPEEP', position=1, golden=golden),
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
    for i in [1, 2, 3]:
        assert board.p1.characters[i].display_name == 'Sheep'
        assert board.p1.characters[i].attack, board.p2.characters[i].health == final_stats

