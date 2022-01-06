import pytest

from sbbbattlesim import Board
from sbbbattlesim.utils import Tribe
from tests import make_character, make_player


def test_slog():
    player = make_player(
        raw=True,
        characters=[
            make_character(
                position=1, attack=1, health=101,
            ),
        ],
    )
    enemy = make_player(
        raw=True,
        treasures=['''SBB_TREASURE_HERMES'BOOTS'''],
        characters=[
            make_character(position=1, attack=1, health=100),
        ],

    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()

    assert board.p1.characters[1].health == 1
