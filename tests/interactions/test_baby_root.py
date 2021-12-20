import pytest

from sbbbattlesim import Board
from tests import make_character, make_player


@pytest.mark.parametrize('golden', (True, False))
def test_baby_root(golden):

    if golden:
        temp_health = 6
        base_health = 1
    else:
        temp_health = 3
        base_health = 4

    player = make_player(
        raw=True,
        characters=[
            make_character(id="SBB_CHARACTER_BABYROOT", position=5, attack=1, health=1, golden=golden),
            make_character(position=1, attack=1, health=7),
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    enemy = make_player()
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=2)
    board.p1.resolve_board()
    board.p2.resolve_board()

    assert board.p1.characters[1]._temp_health == temp_health
    assert board.p1.characters[1]._base_health == base_health
    assert board.p1.characters[1]._base_attack == 1
    assert board.p1.characters[1]._temp_attack == 0
