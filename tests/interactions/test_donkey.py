import pytest

from sbbbattlesim import Board
from tests import make_character, make_player


@pytest.mark.parametrize('golden', (True, False))
@pytest.mark.parametrize('level', (2, 3, 4, 5, 6))
@pytest.mark.parametrize('repeat', range(30))
def test_donkey_surviving(golden, level, repeat):
    player = make_player(
        level=level,
        characters=[
            make_character(id='SBB_CHARACTER_TROJANDONKEY', attack=1, health=3, position=1, golden=golden),
        ],
    )
    enemy = make_player(
        characters=[make_character(attack=1, health=1)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=1)


    assert board.p1.characters[2] is not None
    if golden:
        assert board.p1.characters[2]._level == level
    else:
        assert board.p1.characters[2]._level <= level and board.p1.characters[2]._level > 1
