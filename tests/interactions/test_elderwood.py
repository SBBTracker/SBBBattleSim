import pytest

from sbbbattlesim import Board
from sbbbattlesim.utils import Tribe
from tests import make_character, make_player


@pytest.mark.parametrize('golden', (True, False))
def test_elderwood(golden):
    player = make_player(
        raw=True,
        characters=[
            make_character(id="SBB_CHARACTER_ELDERTREANT", position=5, attack=1, health=1, golden=golden),
            make_character(position=1, attack=1, health=1, tribes=[Tribe.TREANT]),
            make_character(position=2, attack=1, health=1)
        ],
    )
    enemy = make_player(raw=True)
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=0)

    if golden:
        final_stats = (5, 5)
    else:
        final_stats = (3, 3)

    assert (board.p1.characters[1].attack, board.p1.characters[1].health) == final_stats
    assert (board.p1.characters[2].attack, board.p1.characters[2].health) == (1, 1)
