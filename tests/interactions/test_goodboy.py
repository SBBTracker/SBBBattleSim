import pytest

from sbbbattlesim import Board
from sbbbattlesim.utils import Tribe
from tests import make_character, make_player


@pytest.mark.parametrize('golden', (True, False))
def test_goodboy(golden):

    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_GOODBOY', position=1, attack=5, health=5, golden=golden),
            make_character(position=7, tribes=[Tribe.GOOD]),
            make_character(position=6)
        ],
    )
    enemy = make_player(
        characters=[
            make_character(attack=5, health=5),
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=1)
    board.p1.resolve_board()
    board.p2.resolve_board()

    assert (board.p1.characters[7].attack, board.p1.characters[7].health) == (11, 11) if golden else (6, 6)
    assert (board.p1.characters[6].attack, board.p1.characters[6].health) == (1, 1)
