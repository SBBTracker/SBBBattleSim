import pytest

from sbbbattlesim import Board
from tests import make_character, make_player


@pytest.mark.parametrize('golden_grimsoul', (True, False))
@pytest.mark.parametrize('golden_woggle', (True, False))
def test_grimsoul(golden_grimsoul, golden_woggle):
    player = make_player(
        level=2,
        characters=[
            make_character(id='SBB_CHARACTER_CERBERUS', position=1, attack=1, health=1, golden=golden_grimsoul),
            make_character(id='SBB_CHARACTER_BABAYAGA', position=5, attack=3, health=6),
            make_character(id='SBB_CHARACTER_POLYWOGGLE', position=2, attack=1, health=1, golden=golden_woggle),
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

    lvl=3
    if golden_woggle:
        lvl=4

    assert board.p1.characters[2]._level == lvl
