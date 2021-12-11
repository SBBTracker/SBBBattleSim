from sbbbattlesim import Board
from tests import make_character, make_player
import pytest

@pytest.mark.parametrize('mittens', (True, False))
def test_rottenappletree_slay_mittens(mittens):

    player = make_player(
        characters=[
            make_character(id="SBB_CHARACTER_WORLDSERPENT", position=7, attack=40, health=40),
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    enemy = make_player(
        characters=[
            make_character(id="SBB_CHARACTER_ROTTENAPPLETREE", attack=0, health=1),
        ],
        treasures=[
            '''SBB_TREASURE_EXPLODINGMITTENS''' if mittens else ''
        ]
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    jorm = board.p1.characters[7]
    winner, loser = board.fight(limit=1)
    board.p1.resolve_board()
    board.p2.resolve_board()

    assert not jorm.dead, jorm.pretty_print()
