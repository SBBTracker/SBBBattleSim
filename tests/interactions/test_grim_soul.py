import pytest

from sbbbattlesim import Board
from tests import make_character, make_player


@pytest.mark.parametrize('golden', (True, False))
def test_grimsoul(golden):
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_CERBERUS', position=1, attack=1, health=1, golden=golden),
            make_character(id='SBB_CHARACTER_NIGHTSTALKER', position=2, attack=1, health=1, golden=False),
            make_character(id='SBB_CHARACTER_RIVERWISHMERMAID', position=6, attack=1, health=1, golden=False),
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    enemy = make_player(
        characters=[make_character(attack=1, health=1)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=1)
    board.p1.resolve_board()
    board.p2.resolve_board()

    final_stats = (5, 5) if golden else (3, 3)
    assert (board.p1.characters[2].attack, board.p1.characters[2].health) == final_stats



def test_grimsoul_southsea():
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_CERBERUS', position=1, attack=1, health=1),
            make_character(id='SBB_CHARACTER_LOBO', position=2, attack=1, health=1, golden=False),
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    enemy = make_player(
        characters=[make_character(attack=1, health=1)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=1)
    board.p1.resolve_board()
    board.p2.resolve_board()
