from sbbbattlesim import Board
from tests import make_character, make_player
import pytest

@pytest.mark.parametrize('golden', (True, False))
def test_tweedledee(golden):

    player = make_player(
        raw=True,
        characters=[
            make_character(id="SBB_CHARACTER_TWEEDLEDEE", attack=2, health=6, golden=golden),
            make_character(id="SBB_CHARACTER_ECHOWOODSHAMBLER", attack=1, health=1, position=7)
        ]
    )

    enemy = make_player(
        raw=True,
        characters=[make_character(id='Enemy', attack=100, health=100)]
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=1)

    player = board.p1
    tweedle_dum = player.characters[1]
    echowood = player.characters[7]

    assert tweedle_dum
    assert tweedle_dum.attack == (12 if golden else 6)
    assert tweedle_dum.health == (4 if golden else 2)
    assert echowood
    assert echowood.attack == (13 if golden else 7)
    assert echowood.health == (5 if golden else 3)


