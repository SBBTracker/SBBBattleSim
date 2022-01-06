import pytest

from sbbbattlesim import Board
from tests import make_character, make_player


@pytest.mark.parametrize('mimic', (True, False))
def test_simple_drac_sabre(mimic):
    player = make_player(
        raw=True,
        characters=[
            make_character(position=2, attack=5, health=5),
            make_character(position=6, attack=1, health=1),
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS''',
            '''SBB_TREASURE_DRACULA'SSABER''',
            "SBB_TREASURE_TREASURECHEST" if mimic else ''
        ]
    )
    enemy = make_player(
        raw=True,
        characters=[
            make_character(position=1),
            make_character(position=2),
        ],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=3)

    final_stats = (9, 5) if mimic else (5, 3)

    assert (board.p1.characters[6].attack, board.p1.characters[6].health) == final_stats


@pytest.mark.parametrize('direction', (True, False))
def test_proc_order_drac_sabre(direction):
    player = make_player(
        raw=True,
        characters=[
            make_character(position=1, attack=2, health=2),
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS''' if direction else '',
            '''SBB_TREASURE_DRACULA'SSABER'''
        ]
    )
    enemy = make_player(
        raw=True,
        characters=[
            make_character(id="SBB_CHARACTER_WRETCHEDMUMMY", attack=1, health=1, position=1),
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS''' if not direction else '',
        ]
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=1)

    assert (board.p1.characters[1].attack, board.p1.characters[1].health) == (4, 1)
