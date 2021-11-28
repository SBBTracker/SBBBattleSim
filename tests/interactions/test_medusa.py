from sbbbattlesim import Board
from tests import make_character, make_player
import pytest

@pytest.mark.parametrize('golden', (True, False))
def test_medusa(golden):

    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_MEDUSA', position=6, attack=1, health=1, golden=golden),
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    enemy = make_player(
        characters=[make_character(attack=1, health=1)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    creature = board.p2.characters[1]
    winner, loser = board.fight(limit=3)
    statue = board.p2.characters[1]

    board.p1.resolve_board()
    board.p2.resolve_board()

    assert creature is not statue
    assert statue.health == (1 if golden else 4)

