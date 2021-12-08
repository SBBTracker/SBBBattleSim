import pytest

from sbbbattlesim import Board
from tests import make_character, make_player


@pytest.mark.parametrize('golden', (True, False))
@pytest.mark.parametrize('level', (2, 3, 4, 5, 6))
def test_polywoggle(golden, level):
    player = make_player(
        level=level,
        characters=[
            make_character(id='SBB_CHARACTER_POLYWOGGLE', position=2, attack=2, health=2, golden=golden),
            make_character(id='SBB_CHARACTER_NIGHTSTALKER', position=5, attack=1, health=1),
            make_character(id='SBB_CHARACTER_BABAYAGA', position=6, attack=3, health=6, golden=golden),

        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    enemy = make_player(
        characters=[
            make_character(attack=0, health=1, position=1),
            make_character(attack=0, health=1, position=2),
        ],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    woggle = board.p1.characters[5]
    winner, loser = board.fight(limit=3)
    board.p1.resolve_board()
    board.p2.resolve_board()

    golden_promotion = (2 if golden else 1)

    assert (board.p1.characters[5].attack, board.p1.characters[5].health) == (2, 2), 'Vainpire probably didnt attack'
    assert board.p1.characters[2] is not None
    assert board.p1.characters[2] is not woggle, 'Its still the polywoggle unfortunately'
    assert board.p1.characters[2].golden == golden
    assert board.p1.characters[2].cost == min(6, level + golden_promotion)
