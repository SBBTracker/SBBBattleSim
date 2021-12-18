import pytest

from sbbbattlesim import Board
from tests import make_character, make_player


@pytest.mark.parametrize('golden', (True, False))
def test_yaga_slay(golden):
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_BABAYAGA', position=6, attack=3, health=6, golden=golden),
            make_character(id='SBB_CHARACTER_CATBURGLAR', position=2),
            make_character(id="SBB_CHARACTER_SHADOWASSASSIN", position=7, attack=1, health=1)
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    enemy = make_player(
        characters=[make_character(attack=0, health=1)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=1)


    final_stats = (4, 1) if golden else (3, 1)
    assert (board.p1.characters[7].attack, board.p1.characters[7].health) == final_stats


def test_yaga_ranged():
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_BABAYAGA', position=6, attack=3, health=6),
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    enemy = make_player(
        characters=[make_character(attack=1, health=1)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=2)


    assert (board.p1.characters[6].attack, board.p1.characters[6].health) == (3, 6)
