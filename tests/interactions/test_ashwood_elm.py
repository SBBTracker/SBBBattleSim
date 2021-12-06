import pytest

from sbbbattlesim import Board
from sbbbattlesim.utils import Tribe
from tests import make_character, make_player


@pytest.mark.parametrize('golden', (True, False))
def test_ashwood_elm(golden):
    player = make_player(
        characters=[
            make_character(
                id="SBB_CHARACTER_KINGTREE", position=5,
                attack=1, health=100, golden=golden, tribes=[Tribe.TREANT]
            ),
            make_character(position=1, attack=1, health=1, tribes=[Tribe.TREANT]),
            make_character(position=2, attack=1, health=1),
        ],
    )
    enemy = make_player()
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=0)
    board.p1.resolve_board()
    board.p2.resolve_board()

    treant_attack = (201 if golden else 101)

    assert (board.p1.characters[1].attack, board.p1.characters[1].health) == (treant_attack, 1)
    assert (board.p1.characters[2].attack, board.p1.characters[2].health) == (1, 1)
    assert (board.p1.characters[5].attack, board.p1.characters[5].health) == (treant_attack, 100)
