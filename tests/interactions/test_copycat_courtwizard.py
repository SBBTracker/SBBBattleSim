import pytest

from sbbbattlesim import Board
from sbbbattlesim.utils import Tribe
from tests import make_character, make_player


def test_copycat_goes_off_before_courtwizard():
    player = make_player(
        raw=True,
        hero="SBB_HERO_MUERTE",
        characters=[
            make_character(id="SBB_CHARACTER_COPYCAT", position=1, attack=1, health=1),
            make_character(id="SBB_CHARACTER_BLACKCAT", position=5, attack=1, health=1),
            make_character(position=6, attack=1, health=1),
            make_character(position=7, attack=1, health=1),
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    enemy = make_player(
        raw=True,
        characters=[
            make_character(position=1, tribes=[Tribe.PRINCE]),
            make_character(id='SBB_CHARACTER_COURTWIZARD', position=6, attack=1, health=1),

        ],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    p1chars = board.p1.characters
    backline = [p1chars[5], p1chars[6], p1chars[7]]
    winner, loser = board.fight(limit=1)

    assert len(board.p1.graveyard) == 2

    for bl in backline:
        assert not bl.dead


