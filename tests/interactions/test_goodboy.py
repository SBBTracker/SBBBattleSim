import pytest

from sbbbattlesim import Board, configure_logging
from sbbbattlesim.utils import Tribe
from tests import make_character, make_player


@pytest.mark.parametrize('golden', (True, False))
def test_goodboy(golden):
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_GOODBOY', position=1, attack=5, health=5, golden=golden),
            make_character(position=7, tribes=[Tribe.GOOD]),
            make_character(position=6)
        ],
    )
    enemy = make_player(
        characters=[
            make_character(attack=5, health=5),
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=1)


    assert (board.p1.characters[7].attack, board.p1.characters[7].health) == (11, 11) if golden else (6, 6)
    assert (board.p1.characters[6].attack, board.p1.characters[6].health) == (1, 1)


def test_goodboy_mirroruniverse():
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_GOODBOY', position=1, attack=5, health=5, golden=True),
        ],
        treasures=['''SBB_TREASURE_MIRRORUNIVERSE''']
    )
    enemy = make_player(
        characters=[
            make_character(attack=5, health=5),
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=1)


    doggo = board.p1.characters[1]
    assert doggo
    assert doggo.health == 11
    assert doggo.attack == 11


def test_copycat():
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_COPYCAT', position=1, attack=5, health=5),
            make_character(id='SBB_CHARACTER_GOODBOY', position=5, attack=5, health=5, tribes=[Tribe.GOOD]),
            make_character(id='SBB_CHARACTER_GOODBOY', position=6, attack=5, health=5, tribes=[Tribe.GOOD]),
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    enemy = make_player(
        characters=[
            make_character(attack=5, health=5),
        ]
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=1)

    doggo1 = board.p1.characters[5]
    assert doggo1
    assert doggo1.health == 5
    assert doggo1.attack == 5

    doggo2 = board.p1.characters[6]
    assert doggo2
    assert doggo2.health == 10
    assert doggo2.attack == 10
