import pytest

from sbbbattlesim import Board
from tests import make_character, make_player


@pytest.mark.parametrize('golden', (True, False))
@pytest.mark.parametrize('limit', (1, 2))
def test_babybear_dying(golden, limit):

    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_BABYBEAR', position=6,
                           attack=2 if golden else 1, health=2 if golden else 1, golden=golden),
        ],
    )
    enemy = make_player(
        characters=[make_character(attack=500, health=500)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=limit)
    board.p1.resolve_board()
    board.p2.resolve_board()

    if limit == 1:
        assert board.p1.characters[6].__class__.__name__ == 'PapaBear'
    if limit == 2:
        assert board.p1.characters[6].display_name == 'Mama Bear'
