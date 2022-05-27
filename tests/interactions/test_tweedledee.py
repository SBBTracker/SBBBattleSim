import pytest

from sbbbattlesim import fight
from tests import make_character, make_player


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
    fight(player, enemy, limit=1)


    tweedle_dum = player.characters[1]
    echowood = player.characters[7]

    assert tweedle_dum
    assert tweedle_dum.attack == (12 if golden else 6)
    assert tweedle_dum.health == (4 if golden else 2)
    assert echowood
    assert echowood.attack == (13 if golden else 7)
    assert echowood.health == (5 if golden else 3)


@pytest.mark.parametrize('golden', (True, False))
def test_tweedledee_sting(golden):

    player = make_player(
        raw=True,
        characters=[
            make_character(id="SBB_CHARACTER_TWEEDLEDEE", attack=12, health=6, golden=golden),
            make_character(id="SBB_CHARACTER_ECHOWOODSHAMBLER", attack=1, health=1, position=7)
        ],
        treasures=['SBB_TREASURE_STING']
    )

    enemy = make_player(
        raw=True,
        characters=[make_character(id='Enemy', attack=100, health=100)]
    )
    fight(player, enemy, limit=1)


    tweedle_dum = player.characters[1]
    echowood = player.characters[7]

    assert tweedle_dum
    assert not tweedle_dum.dead
    assert tweedle_dum.attack == (22 if golden else 16)
    assert tweedle_dum.health == (24 if golden else 12)
    assert echowood
    assert echowood.attack == (23 if golden else 17)
    assert echowood.health == (25 if golden else 13)


@pytest.mark.parametrize('golden', (True, False))
def test_tweedledee_helm(golden):

    player = make_player(
        raw=True,
        characters=[
            make_character(id="SBB_CHARACTER_TWEEDLEDEE", attack=2, health=12, golden=golden),
            make_character(id="SBB_CHARACTER_ECHOWOODSHAMBLER", attack=1, health=1, position=7)
        ],
        treasures=['SBB_TREASURE_STONEHELM']
    )

    enemy = make_player(
        raw=True,
        characters=[make_character(id='Enemy', attack=100, health=100)]
    )
    fight(player, enemy, limit=1)


    tweedle_dum = player.characters[1]
    echowood = player.characters[7]

    assert tweedle_dum
    assert not tweedle_dum.dead
    assert tweedle_dum.attack == (24 if golden else 12)
    assert tweedle_dum.health == (14 if golden else 12)
    assert echowood
    assert echowood.attack == (25 if golden else 13)
    assert echowood.health == (15 if golden else 13)


def test_tweedledee_shrivel():

    player = make_player(
        raw=True,
        characters=[
            make_character(id="SBB_CHARACTER_TWEEDLEDEE", attack=1, health=1),
        ]
    )

    enemy = make_player(
        raw=True,
        characters=[make_character()],
        spells=['SBB_SPELL_ENFEEBLEMENT']
    )
    fight(player, enemy, limit=1)



    assert not player.characters[1].dead
    assert player.characters[1].attack == 0
    assert player.characters[1].health == 0