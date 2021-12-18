import pytest

from sbbbattlesim import Board
from tests import make_character, make_player


@pytest.mark.parametrize('golden', (True, False))
def test_baby_root(golden):
    player = make_player(
        characters=[
            make_character(id="SBB_CHARACTER_BABYROOT", position=5, attack=1, health=1, golden=golden),
            make_character(position=1, attack=1, health=1),
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    enemy = make_player()
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=2)


    if golden:
        final_stats = (1, 7)
    else:
        final_stats = (1, 4)

    assert (board.p1.characters[1].attack, board.p1.characters[1].health) == final_stats
