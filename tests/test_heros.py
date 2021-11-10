from sbbbattlesim import Board
from sbbbattlesim.utils import Tribe, Keyword
from tests import make_character, make_player


def test_evella():
    player = make_player(
        characters=[make_character(id='GENERIC', position=i, keywords=[kw.value for kw in Keyword], tribes=[tribe.value for tribe in Tribe]) for i in range(1, 8)],
        hero='SBB_HERO_DARKONE'
    )
    enemy = make_player(
        characters=[make_character(id='GENERIC', position=i) for i in range(1, 8)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()

    player = board.p1
