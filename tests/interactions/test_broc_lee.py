from sbbbattlesim import Board
from tests import make_character, make_player
import pytest

@pytest.mark.parametrize('golden', (True, False))
def test_broc_lee(golden):

    player = make_player(
        characters=[
            make_character(id="SBB_CHARACTER_RAZORLEAFOAK", position=1, attack=0, health=100, golden=golden),
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    enemy = make_player(
        characters=[
            make_character(attack=1, health=1, position=1),
            make_character(attack=1, health=1, position=2)
        ],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=-1)
    board.p1.resolve_board()
    board.p2.resolve_board()

    assert board.p1.characters[1].attack == (60 if golden else 30)

