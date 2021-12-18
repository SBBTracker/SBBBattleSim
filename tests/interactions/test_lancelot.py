import pytest

from sbbbattlesim import Board
from tests import make_character, make_player


@pytest.mark.parametrize('golden', (True, False))
def test_lancelot(golden):
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_LANCELOT', position=6, attack=1, health=1, golden=golden),
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


    final_stats = (5, 5) if golden else (3, 3)
    assert (board.p1.characters[6].attack, board.p1.characters[6].health) == final_stats
