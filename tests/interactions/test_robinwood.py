import pytest

from sbbbattlesim import Board
from sbbbattlesim.utils import Tribe
from tests import make_character, make_player


@pytest.mark.parametrize('golden', (True, False))
def test_robinwood(golden):
    player = make_player(
        characters=[
            make_character(
                id="SBB_CHARACTER_ROBINWOOD", position=5,
                attack=5, health=1, golden=golden, tribes=[Tribe.TREANT]
            ),
            make_character(position=2, attack=2, health=1),
        ],
    )
    enemy = make_player(
        characters=[
            make_character(position=1, attack=20),
            make_character(position=2, attack=5)
        ]
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=0)


    buffed_attack = (32 if golden else 17)

    assert (board.p1.characters[2].attack, board.p1.characters[2].health) == (buffed_attack, 1)
    assert (board.p1.characters[5].attack, board.p1.characters[5].health) == (5, 1)

    assert board.p2.characters[1].attack == (0 if golden else 5)
    assert board.p2.characters[2].attack == 5


def test_robinwood_ranged():
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_ROBINWOOD', position=6, attack=3, health=6),
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


    assert (board.p1.characters[6].attack, board.p1.characters[6].health) == (18, 6)
