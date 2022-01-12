import pytest

from sbbbattlesim import Board
from sbbbattlesim.utils import Tribe
from tests import make_character, make_player


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


    assert board.p1.characters[1]._level == 1
    assert board.p1.characters[2]._level == 2
    assert board.p1.characters[3]._level == 3
    assert board.p1.characters[4]._level == 4

@pytest.mark.parametrize('golden', (True, False))
def test_pumpkin_summoning_cats(golden):
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_PUMPKINKING', position=5, tribes=[Tribe.EVIL], golden=golden),
            make_character(position=1, _level=2, tribes=[Tribe.EVIL]),
        ],
    )
    enemy = make_player(
        characters=[make_character(attack=500, health=500)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    pk = board.p1.characters[1]
    winner, loser = board.fight(limit=2)


    summoned_unit = board.p1.characters[1]
    assert summoned_unit, [i.pretty_print() for i in board.p1.valid_characters()]
    assert summoned_unit.id == "SBB_CHARACTER_CAT"
    assert summoned_unit.golden == golden


@pytest.mark.parametrize('golden', (True, False))
@pytest.mark.parametrize('r', range(30))
def test_pumpkin_summoning_two_cats(golden, r):
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_PUMPKINKING', position=5, tribes=[Tribe.EVIL], golden=golden),
            make_character(id='SBB_CHARACTER_BLACKCAT', position=1, _level=2, tribes=[Tribe.EVIL]),
            make_character(id='SBB_CHARACTER_PROSPERO', position=7)
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    enemy = make_player(
        characters=[make_character(attack=500, health=500)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    board.p1.characters[5]._level = 0  # hacky fix
    pk = board.p1.characters[1]
    winner, loser = board.fight(limit=3)

    for pos in [1, 2]:
        summoned_unit = board.p1.characters[pos]
        assert summoned_unit, [i.pretty_print() for i in board.p1.valid_characters()]
        assert summoned_unit.id == "SBB_CHARACTER_CAT"
        assert summoned_unit.golden == golden
        assert summoned_unit.health == (8 if golden else 6)
        assert summoned_unit.attack == (8 if golden else 6)

