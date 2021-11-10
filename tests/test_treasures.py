import pytest

from sbbbattlesim import Board
from sbbbattlesim.utils import Keyword, Tribe
from tests import make_character, make_player, get_treasures


@pytest.mark.parametrize('mimic', (True, False))
@pytest.mark.parametrize('treasure', get_treasures())
def test_treasure(treasure, mimic):
    generic_char = make_character(id='GENERIC', attack=1, position=7, keywords=[kw for kw in Keyword],
                                  tribes=[tribe for tribe in Tribe])
    player = make_player(
        characters=[generic_char],
    )
    enemy = make_player(
        characters=[make_character(id='SBB_CHARACTER_MONSTAR', position=1, attack=1, health=1)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
