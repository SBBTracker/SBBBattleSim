import pytest

from sbbbattlesim import Board
from sbbbattlesim.utils import Tribe
from tests import make_character, make_player


@pytest.mark.parametrize('golden', (True, False))
def test_rainbow_unicorn(golden):
    player = make_player(
        characters=[
            make_character(
                id="SBB_CHARACTER_HELPFULGODMOTHER", position=5, attack=1,
                health=1, golden=golden, tribes=[Tribe.GOOD]
            ),
            make_character(position=6, attack=1, health=1, tribes=[Tribe.GOOD]),
            make_character(position=7, attack=1, health=1)
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    enemy = make_player()
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=0)
    board.p1.resolve_board()
    board.p2.resolve_board()

    if golden:
        final_stats = (1, 3)
    else:
        final_stats = (1, 2)

    assert (board.p1.characters[6].attack, board.p1.characters[6].health) == final_stats
    assert (board.p1.characters[7].attack, board.p1.characters[7].health) == (1, 1)
    assert (board.p1.characters[5].attack, board.p1.characters[5].health) == (1, 1)
