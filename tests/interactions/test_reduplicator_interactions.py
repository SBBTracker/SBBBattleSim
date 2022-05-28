import pytest

from sbbbattlesim import fight
from tests import make_character, make_player


def test_reduplicator_bearstain():

    player = make_player(
        characters=[
            make_character(id="SBB_CHARACTER_BLACKCAT", position=1, health=1),
            make_character(id="SBB_CHARACTER_PROSPERO", position=7, health=1),
        ],
        treasures=[
            'SBB_TREASURE_REDUPLICATOR',
        ]
    )

    enemy = make_player(
        spells=[
            "SBB_SPELL_EARTHQUAKE"
        ]
    )
    fight(player, enemy)



    char1 = player.characters[1]
    char2 = player.characters[2]

    assert char1
    assert char2
    assert char1.id == char2.id

    assert (char1.attack, char1.health) == (6, 6)
    assert (char1.attack, char1.health) == (char2.attack, char2.health)


def test_reduplicator_craft():

    player = make_player(
        characters=[
            make_character(id="SBB_CHARACTER_DWARVENARTIFICER", position=1, attack=1, health=1),
        ],
        treasures=[
            'SBB_TREASURE_MIRRORUNIVERSE',
            'SBB_TREASURE_REDUPLICATOR',
        ]
    )

    enemy = make_player(
        characters=[make_character(attack=50, health=50)]
    )
    fight(player, enemy, limit=1)



    char1 = player.characters[1]
    char2 = player.characters[2]

    assert char1
    assert char2
    assert char1.id == char2.id

    assert (char1.attack, char1.health) == (5, 5)
    assert (char1.attack, char1.health) == (char2.attack, char2.health)


def test_reduplicator_juliet():

    player = make_player(
        characters=[
            make_character(id="SBB_CHARACTER_JULIET", position=1, health=1),
            make_character(id="SBB_CHARACTER_ROMEO", position=2, health=1)
        ],
        treasures=[
            'SBB_TREASURE_REDUPLICATOR',
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )

    enemy = make_player(
        characters=[make_character(attack=50, health=50)]
    )
    fight(player, enemy, limit=2)



    char1 = player.characters[2]
    char2 = player.characters[3]

    assert char1
    assert char2
    assert char1.id == char2.id

    assert char1.id == char2.id == "SBB_CHARACTER_JULIET"
    assert (char1.attack, char1.health) == (8, 8)
    assert (char1.attack, char1.health) == (char2.attack, char2.health)


@pytest.mark.parametrize('r', range(30))
def test_reduplicator_wombat(r):

    player = make_player(
        level=3,
        characters=[
            make_character(id="SBB_CHARACTER_WOMBATSINDISGUISE", attack=1, health=1, position=1),
        ],
        treasures=[
            'SBB_TREASURE_REDUPLICATOR',
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )

    enemy = make_player(
        characters=[make_character(attack=50, health=50)]
    )
    fight(player, enemy, limit=1)



    char1 = player.characters[1]
    char2 = player.characters[2]

    assert char1
    assert char2

    assert char1.attack != char1._attack, char1.pretty_print()
    assert char1.health != char1._health, char1.pretty_print()
    assert (char1.attack, char1.health) == (char2.attack, char2.health), char2.pretty_print()


def test_reduplicator_puffpuff():

    player = make_player(
        characters=[
            make_character(id="SBB_CHARACTER_PUFFPUFF", attack=10, health=10),
        ],
        treasures=[
            'SBB_TREASURE_MIRRORUNIVERSE',
            'SBB_TREASURE_REDUPLICATOR',
        ]
    )

    enemy = make_player(
        characters=[make_character(attack=50, health=50)]
    )
    fight(player, enemy, limit=1)



    char1 = player.characters[1]
    char2 = player.characters[2]

    assert char1, f'{[c.pretty_print() for c in player.valid_characters()]}'
    assert char2, f'{[c.pretty_print() for c in player.valid_characters()]}'
    assert char1.id == char2.id

    assert (char1.attack, char1.health) == (5, 5)
    assert (char1.attack, char1.health) == (char2.attack, char2.health)


def test_reduplicator_stormking():

    player = make_player(
        characters=[
            make_character(id="SBB_CHARACTER_THEGREATANDPOWERFUL", attack=10, health=10),
        ],
        treasures=[
            'SBB_TREASURE_MIRRORUNIVERSE',
            'SBB_TREASURE_REDUPLICATOR',
        ]
    )

    enemy = make_player(
        characters=[make_character(attack=50, health=50)]
    )
    fight(player, enemy, limit=1)



    char1 = player.characters[1]
    char2 = player.characters[2]

    assert char1, f'{[c.pretty_print() for c in player.valid_characters()]}'
    assert char2, f'{[c.pretty_print() for c in player.valid_characters()]}'
    assert char1.id == char2.id

    assert (char1.attack, char1.health) == (9, 9)
    assert (char1.attack, char1.health) == (char2.attack, char2.health)


@pytest.mark.parametrize('expend', (True, False))
def test_reduplicator_does_it_waste(expend):
    characters=[
        make_character(id="SBB_CHARACTER_PRINCESSPEEP", position=1, attack=1, health=1),
        make_character(position=5, attack=1, health=1),
        make_character(position=6, attack=1, health=1),
        make_character(position=7, attack=1, health=1),
    ]
    if not expend:
        characters.append(make_character(position=4, attack=1, health=1))

    player = make_player(
        characters=characters,
        treasures=[
            'SBB_TREASURE_REDUPLICATOR',
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )

    enemy = make_player(
        characters=[make_character(attack=50, health=50)]
    )
    fight(player, enemy, limit=1)


    triggered = player.treasures['SBB_TREASURE_REDUPLICATOR'][0].triggered
    if expend:
        assert triggered
    else:
        assert not triggered
