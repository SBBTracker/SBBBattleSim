import pytest

from sbbbattlesim import fight
from sbbbattlesim.utils import Tribe
from tests import make_character, make_player


@pytest.mark.parametrize('golden', (False, True))
def test_muerte_copycat_goodboy(golden):
    player = make_player(
        raw=True,
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
        raw=True,
        characters=[
            make_character(),
            make_character()
        ],
    )
    fight(player, enemy, limit=1)

    if golden:
        final_stats = (31, 31)
    else:
        final_stats = (9, 9)

    assert (player.characters[5].attack, player.characters[5].health) == final_stats


@pytest.mark.parametrize('golden', (True, False))
def test_muerte_single_goodboy(golden):
    player = make_player(
        raw=True,
        hero="SBB_HERO_MUERTE",
        characters=[
            make_character(position=5, attack=1, health=1, tribes=[Tribe.GOOD]),
            make_character(id="SBB_CHARACTER_GOODBOY", position=1, attack=1, health=1, tribes=[Tribe.GOOD], golden=golden),
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    enemy = make_player(
        raw=True,
        characters=[
            make_character()
        ],
    )
    fight(player, enemy, limit=1)

    if golden:
        final_stats = (5, 5)
    else:
        final_stats = (3, 3)

    assert (player.characters[5].attack, player.characters[5].health) == final_stats


def test_copycat_queenofhearts():
    '''Copycat should not trigger queenofhearts ondeath buff'''
    player = make_player(
        raw=True,
        hero="SBB_HERO_MUERTE",
        characters=[
            make_character(id="SBB_CHARACTER_COPYCAT", position=2, attack=1, health=5),
            make_character(id="SBB_CHARACTER_GOODBOY", position=5, attack=1, health=1, tribes=[Tribe.EVIL]),
            make_character(id="SBB_CHARACTER_QUEENOFHEARTS", position=7, attack=1, health=1, golden=True),
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    enemy = make_player(
        raw=True,
        characters=[
            make_character()
        ],
    )
    fight(player, enemy, limit=1)

    assert len(
        [evt for evt in player.characters[5].get('OnDeath') if evt.__class__.__name__ == 'EvilQueenOnDeath']) == 1
    assert (player.characters[7].attack, player.characters[7].health) == (1, 1)
