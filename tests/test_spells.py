import pytest

from sbbbattlesim import Board
from sbbbattlesim.utils import Keyword, Tribe, StatChangeCause
from tests import make_character, make_player, get_spells


@pytest.mark.parametrize('spell', get_spells())
def test_character(spell):
    player = make_player(
        characters=[make_character(id='GENERIC', attack=1, position=1, keywords=[kw.value for kw in Keyword], tribes=[tribe.value for tribe in Tribe])],
        spells=[spell]
    )
    enemy = make_player(
        characters=[make_character(id='SBB_CHARACTER_MONSTAR', position=1, attack=1, health=1)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=-1)