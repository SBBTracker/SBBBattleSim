import pytest

from sbbbattlesim import Board
from tests import make_character, make_player


@pytest.mark.parametrize('golden', (True, False))
def test_threebigpigs(golden):
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_THREEBIGPIGS', position=1, golden=golden),
        ],
        hand=['SBB_SPELL_FOO', 'SBB_CHARACTER_THREEBIGPIGS']
    )
    enemy = make_player(
        characters=[make_character(attack=500, health=500)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=1)


    final_stats = (2, 2) if golden else (1, 1)
    for i in [1, 2, 3]:
        assert board.p1.characters[i].id == 'SBB_CHARACTER_PIGGY', board.p1.characters[i].pretty_print()
        assert board.p1.characters[i].attack, board.p2.characters[i].health == final_stats
