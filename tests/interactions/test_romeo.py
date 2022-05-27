import pytest

from sbbbattlesim import fight
from tests import make_character, make_player


@pytest.mark.parametrize('golden', (True, False))
def test_romeo_summons_dead_juliet(golden):
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_ROMEO', position=6, attack=1, health=1, golden=golden),
            make_character(id='SBB_CHARACTER_JULIET', attack=7, health=7, position=2),
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    enemy = make_player(
        characters=[make_character(attack=7, health=8)],
    )
    juliet = player.characters[2]
    fight(player, enemy, limit=2)


    final_stats = (21, 21) if golden else (14, 14)
    assert (player.characters[6].attack, player.characters[6].health) == final_stats
    assert player.characters[6].id == juliet.id


def test_romeo_summons_dead_juliet():
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_ROMEO', position=5, attack=1, health=1),
            make_character(id='SBB_CHARACTER_JULIET', attack=7, health=7, position=1),
        ],
    )
    enemy = make_player(
        characters=[make_character(id="SBB_CHARACTER_DOOMBREATH", attack=7, health=7)],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )

    fight(player, enemy, limit=2)

    assert player.characters[5].id == 'SBB_CHARACTER_JULIET'
    assert player.characters[1] is None


def test_romeo_summons_dead_juliet_with_mihri():
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_ROMEO', position=5, attack=2, health=3),
            make_character(id='SBB_CHARACTER_JULIET', attack=2, health=3, position=1),
        ],
        hero='SBB_HERO_KINGLION',
        mihri_buff=1,
        raw=True
    )
    enemy = make_player(
        raw=True,
        characters=[make_character(id="SBB_CHARACTER_DOOMBREATH", attack=7, health=7)],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    fight(player, enemy, limit=1)

    juliet = player.characters[5]
    assert juliet.attack == 9
    assert juliet.health == 10
    assert player.characters[1] is None


def test_romeo_doesnt_summon_anything():
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_ROMEO', position=6, attack=1, health=1),
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    enemy = make_player(
        characters=[make_character(attack=7, health=8)],
    )
    juliet = player.characters[2]
    fight(player, enemy, limit=2)


    assert player.characters[6] is None


def test_two_romeo_summons_one_dead_juliet():
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_ROMEO', position=3, attack=1, health=1),
            make_character(id='SBB_CHARACTER_ROMEO', position=7, attack=1, health=1),
            make_character(id='SBB_CHARACTER_JULIET', attack=7, health=7, position=2),
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    enemy = make_player(
        characters=[make_character(attack=7, health=8)],
    )
    juliet = player.characters[2]
    fight(player, enemy, limit=2)


    assert (player.characters[3].attack, player.characters[3].health) == (14, 14)
    assert player.characters[3].id == juliet.id


def test_two_romeo_summons_dead_juliet_alot():
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_ROMEO', position=3, attack=1, health=1),
            make_character(id='SBB_CHARACTER_ROMEO', position=7, attack=1, health=1),
            make_character(id='SBB_CHARACTER_JULIET', attack=7, health=7, position=2),
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    enemy = make_player(
        characters=[make_character(attack=50, health=50)],
    )
    juliet = player.characters[2]
    fight(player, enemy, limit=4)


    assert (player.characters[7].attack, player.characters[7].health) == (21, 21)
    assert player.characters[7].id == juliet.id


def test_romeo_muerte_summons_dead_juliet():
    player = make_player(
        hero="SBB_HERO_MUERTE",
        characters=[
            make_character(id='SBB_CHARACTER_ROMEO', position=2, attack=1, health=1),
            make_character(id='SBB_CHARACTER_JULIET', attack=7, health=7, position=1),
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    enemy = make_player(
        characters=[make_character(attack=7, health=8)],
    )
    juliet = player.characters[1]
    fight(player, enemy, limit=2)


    assert (player.characters[2].attack, player.characters[2].health) == (14, 14)
    assert player.characters[2].id == juliet.id
    assert (player.characters[3].attack, player.characters[3].health) == (14, 14)
    assert player.characters[3].id == juliet.id


@pytest.mark.parametrize('attackfirst', (True, False))
def test_romeo_always_summons_juliet(attackfirst):
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_ROMEO', position=5, attack=1, health=1),
            make_character(id='SBB_CHARACTER_JULIET', attack=7, health=7, position=1),
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS''' if not attackfirst else ''
        ]
    )
    enemy = make_player(
        characters=[make_character(id="SBB_CHARACTER_WRETCHEDMUMMY", attack=7, health=7)],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS''' if attackfirst else ''
        ]
    )

    fight(player, enemy, limit=2)

    assert player.characters[5].id == 'SBB_CHARACTER_JULIET'
    assert player.characters[1] is None
