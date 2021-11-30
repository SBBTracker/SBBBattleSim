from sbbbattlesim import Board
from tests import make_character, make_player
import pytest
from sbbbattlesim.utils import Tribe

@pytest.mark.parametrize('golden', (True, False))
def test_lonely_pumpkin_dying(golden):

    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_PUMPKINKING', position=1, tribes=[Tribe.EVIL], golden=golden),
        ],
    )
    enemy = make_player(
        characters=[make_character(attack=500, health=500)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    pk = board.p1.characters[1]
    winner, loser = board.fight(limit=1)
    board.p1.resolve_board()
    board.p2.resolve_board()

    summoned_unit = board.p1.characters[1]
    assert summoned_unit is not pk
    assert summoned_unit._level == 5
    if golden:
        assert summoned_unit.attack == summoned_unit._attack * 2
        assert summoned_unit.health == summoned_unit._health * 2


def test_pumpkin_with_friends_dying():

    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_PUMPKINKING', position=7, tribes=[Tribe.EVIL]),
            make_character(position=1, tribes=[Tribe.EVIL]),
            make_character(position=2, tribes=[Tribe.EVIL]),
            make_character(position=3, tribes=[Tribe.EVIL]),
            make_character(position=4, tribes=[Tribe.EVIL]),
        ],
    )
    enemy = make_player(
        characters=[make_character(attack=500, health=500)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    pk = board.p1.characters[1]

    board.p1.characters[1]._level = 2
    board.p1.characters[2]._level = 3
    board.p1.characters[3]._level = 4
    board.p1.characters[4]._level = 5


    winner, loser = board.fight(limit=5)
    board.p1.resolve_board()
    board.p2.resolve_board()

    assert board.p1.characters[1] is None
    assert board.p1.characters[2]._level == 2
    assert board.p1.characters[3]._level == 3
    assert board.p1.characters[4]._level == 4



