import pytest

from sbbbattlesim import Board
from sbbbattlesim.utils import Tribe
from tests import make_character, make_player


@pytest.mark.parametrize('r', range(30))
def test_falling_stars_guides_eventorder(r):
    player = make_player(
        raw=True,
        characters=[
            make_character(position=3, id='SBB_CHARACTER_GOODBOY'),
            make_character(position=2, id='SBB_CHARACTER_WRETCHEDMUMMY'),
            make_character(position=1, id='P1TESTCHAR', tribes={Tribe.GOOD}, health=2),
        ],
        spells=['''SBB_SPELL_FALLINGSTARS''', ]
    )
    enemy = make_player(
        raw=True,
        characters=[
            make_character(position=3, id='SBB_CHARACTER_GOODBOY'),
            make_character(position=2, id='SBB_CHARACTER_WRETCHEDMUMMY'),
            make_character(position=1, id='P2TESTCHAR', tribes={Tribe.GOOD}, health=2),
        ],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=0)

    livingchar = board.p1.characters[1]
    assert livingchar, ([i.pretty_print() for i in board.p1.valid_characters()], [i.pretty_print() for i in board.p2.valid_characters()])
    assert livingchar.attack == 2
    assert livingchar.health == 1

    assert len(board.p2.graveyard) == 3
