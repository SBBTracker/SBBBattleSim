import pytest

from sbbbattlesim import Board
from tests import make_character, make_player


@pytest.mark.parametrize('golden', (True, False))
def test_sporko(golden):
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_MAGEMASTER', position=5, attack=3, health=6, golden=golden),
            make_character(position=2),
            make_character(position=1)
        ]
    )
    enemy = make_player()
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight()
    board.p1.resolve_board()
    board.p2.resolve_board()

    final_attack = (11 if golden else 6)
    assert (board.p1.characters[1].attack, board.p1.characters[1].health) == (final_attack, 1)
    assert (board.p1.characters[2].attack, board.p1.characters[2].health) == (final_attack, 1)


def test_sporko_ranged():
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_MAGEMASTER', position=6, attack=3, health=6),
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
    board.p1.resolve_board()
    board.p2.resolve_board()

    assert (board.p1.characters[6].attack, board.p1.characters[6].health) == (3, 6)
