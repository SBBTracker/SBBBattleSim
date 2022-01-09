from sbbbattlesim import Board
from sbbbattlesim.utils import Tribe
from sbbbattlesim.events import OnDamagedAndSurvived, OnSummon
from tests import make_character, make_player
from sbbbattlesim.characters import registry as character_registry

import pytest


def test_advanced_respawn():
    player = make_player(
        raw=True,
        characters=[
            make_character(id='SBB_CHARACTER_DUMBLEDWARF', position=1, attack=5, health=1),
        ],
        treasures=[
            'SBB_TREASURE_TREASURECHEST',
            "SBB_TREASURE_PHOENIXFEATHER",
            "SBB_TREASURE_WHIRLINGBLADES"
        ]
    )
    enemy = make_player(
        raw=True,
        characters=[make_character()],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    board.fight()

    assert board.p1.treasures['SBB_TREASURE_PHOENIXFEATHER'][0].feather_used

    assert (board.p1.characters[1].attack, board.p1.characters[1].health) == (5, 1)
    assert (board.p1.characters[2].attack, board.p1.characters[2].health) == (5, 1)