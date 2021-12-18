import pytest

from sbbbattlesim import Board
from sbbbattlesim.utils import Tribe
from tests import make_character, make_player


@pytest.mark.parametrize('golden', (True, False))
def test_muerte_copycat_goodboy(golden):
    player = make_player(
        hero="SBB_HERO_MUERTE",
        characters=[
            make_character(id="SBB_CHARACTER_COPYCAT", position=2, attack=1, health=5, golden=golden),
            make_character(id="SBB_CHARACTER_GOODBOY", position=5, attack=1, health=1, tribes=[Tribe.GOOD]),
            make_character(id="SBB_CHARACTER_GOODBOY", position=6, attack=1, health=1, tribes=[Tribe.GOOD],
                           golden=True),
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    enemy = make_player(
        characters=[
            make_character(),
            make_character()
        ],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=2)

    if golden:
        final_stats = (108, 108)
    else:
        final_stats = (18, 18)

    assert (board.p1.characters[6].attack, board.p1.characters[6].health) == final_stats


@pytest.mark.parametrize('golden', (True, False))
def test_muerte_single_goodboy(golden):
    player = make_player(
        hero="SBB_HERO_MUERTE",
        characters=[
            make_character(id="SBB_CHARACTER_COPYCAT", position=2, attack=1, health=5, golden=golden),
            make_character(id="SBB_CHARACTER_GOODBOY", position=5, attack=1, health=1, tribes=[Tribe.GOOD],
                           golden=True),
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    enemy = make_player(
        characters=[
            make_character(),
            make_character()
        ],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=2)


    if golden:
        final_stats = (27, 27)
    else:
        final_stats = (9, 9)

    assert (board.p1.characters[5].attack, board.p1.characters[5].health) == final_stats


def test_copycat_queenofhearts():
    '''Copycat should not trigger queenofhearts ondeath buff'''
    player = make_player(
        hero="SBB_HERO_MUERTE",
        characters=[
            make_character(id="SBB_CHARACTER_COPYCAT", position=2, attack=1, health=5),
            make_character(id="SBB_CHARACTER_GOODBOY", position=5, attack=1, health=1, tribes=[Tribe.EVIL]),
            make_character(id="SBB_CHARACTER_QUEENOFHEARTS", position=7, attack=1, health=1, golden=True),
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    enemy = make_player(
        characters=[
            make_character()
        ],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=1)


    assert len(
        [evt for evt in board.p1.characters[5].get('OnDeath') if evt.__class__.__name__ == 'EvilQueenOnDeath']) == 1
    assert (board.p1.characters[7].attack, board.p1.characters[7].health) == (1, 1)
