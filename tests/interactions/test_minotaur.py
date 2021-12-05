import pytest

from sbbbattlesim import Board
from sbbbattlesim.utils import Tribe
from tests import make_character, make_player


@pytest.mark.parametrize('golden', (True, False))
def test_minotaur(golden):
    player = make_player(
        characters=[
            make_character(
                id="SBB_CHARACTER_LABYRINTHMINOTAUR", tribes=[Tribe.EVIL],
                position=5, attack=1, health=1, golden=golden
            ),
            make_character(position=6, attack=1, health=1, tribes=[Tribe.EVIL]),
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
        final_stats = (3, 1)
    else:
        final_stats = (2, 1)

    assert (board.p1.characters[6].attack, board.p1.characters[6].health) == final_stats
    assert (board.p1.characters[7].attack, board.p1.characters[7].health) == (1, 1)
    assert (board.p1.characters[5].attack, board.p1.characters[5].health) == (1, 1)
