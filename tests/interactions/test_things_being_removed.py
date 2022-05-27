from sbbbattlesim import fight
from tests import make_character, make_player


def test_yaga_dies():
    player = make_player(
        raw=True,
        characters=[
            make_character(id='SBB_CHARACTER_BABAYAGA', position=6, attack=3, health=6),
            make_character(id='SBB_CHARACTER_CATBURGLAR', attack=4, health=1, position=2),
            make_character(id="SBB_CHARACTER_SHADOWASSASSIN", position=4, attack=1, health=1)
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    enemy = make_player(
        characters=[
            make_character(attack=0, health=1),
            make_character(id='SBB_CHARACTER_LIGHTNINGDRAGON', attack=100, health=1, position=7)
        ],
    )
    fight(player, enemy, limit=1)

    final_stats = (2, 1)
    assert player.characters[6] is None
    assert (player.characters[4].attack, player.characters[4].health) == final_stats

    assert player.characters[2].attack == 1


def test_riverwish_dies():
    player = make_player(
        raw=True,
        characters=[
            make_character(id='SBB_CHARACTER_RIVERWISHMERMAID', position=6, attack=3, health=6),
            make_character(id='SBB_CHARACTER_CATBURGLAR', attack=1, health=1, position=2),
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    enemy = make_player(
        characters=[
            make_character(attack=0, health=1),
            make_character(id='SBB_CHARACTER_LIGHTNINGDRAGON', attack=100, health=1, position=7)
        ],
    )
    fight(player, enemy, limit=1)

    final_stats = (1, 1)
    assert player.characters[6] is None
    assert (player.characters[2].attack, player.characters[2].health) == final_stats


def test_darkwood_dies():
    player = make_player(
        raw=True,
        characters=[
            make_character(id='SBB_CHARACTER_DARKWOODCREEPER', position=6, attack=3, health=6),
            make_character(id='SBB_CHARACTER_CATBURGLAR', attack=2, health=2, position=2),
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    enemy = make_player(
        characters=[
            make_character(attack=1, health=1),
            make_character(id='SBB_CHARACTER_LIGHTNINGDRAGON', attack=100, health=1, position=7)
        ],
    )
    fight(player, enemy, limit=1)

    final_stats = (2, 1)
    assert player.characters[6] is None
    assert (player.characters[2].attack, player.characters[2].health) == final_stats

def test_queenofhearts_dies():
    player = make_player(
        raw=True,
        characters=[
            make_character(id='SBB_CHARACTER_QUEENOFHEARTS', position=6, attack=3, health=6),
            make_character(tribes=['evil'], attack=1, health=1, position=2),
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    enemy = make_player(
        characters=[
            make_character(attack=1, health=1),
            make_character(id='SBB_CHARACTER_LIGHTNINGDRAGON', attack=100, health=1, position=7)
        ],
    )
    qoh = player.characters[6]
    fight(player, enemy, limit=1)

    assert qoh.attack == 3
    assert qoh._base_health == 6


def test_support_dies():
    player = make_player(
        raw=True,
        characters=[
            make_character(id='SBB_CHARACTER_BABYROOT', position=6, attack=3, health=6),
            make_character(attack=1, health=4, position=2),
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    enemy = make_player(
        characters=[
            make_character(attack=0, health=1),
            make_character(id='SBB_CHARACTER_LIGHTNINGDRAGON', attack=100, health=1, position=7)
        ],
    )
    fight(player, enemy, limit=1)

    final_stats = (1, 1)
    assert player.characters[6] is None
    assert (player.characters[2].attack, player.characters[2].health) == final_stats


def test_aura_dies():
    player = make_player(
        raw=True,
        characters=[
            make_character(id='SBB_CHARACTER_BIGBOSS', position=6, attack=3, health=6),
            make_character(attack=5, health=5, position=2, tribes=['dwarf']),
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    enemy = make_player(
        characters=[
            make_character(attack=0, health=1),
            make_character(id='SBB_CHARACTER_LIGHTNINGDRAGON', attack=100, health=1, position=7)
        ],
    )
    fight(player, enemy, limit=1)

    final_stats = (2, 2)
    assert player.characters[6] is None
    assert (player.characters[2].attack, player.characters[2].health) == final_stats


def test_supported_unit_dies_and_comes_back():
    player = make_player(
        raw=True,
        characters=[
            make_character(id='SBB_CHARACTER_BABYROOT', position=6, attack=3, health=6),
            make_character(id='SBB_CHARACTER_ECHOWOODSHAMBLER', position=7, attack=1, health=1),
            make_character(attack=100, health=4, position=2),
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS''',
            '''SBB_TREASURE_PHOENIXFEATHER'''
        ]
    )
    enemy = make_player(
        characters=[
            make_character(attack=100, health=1),
        ],
    )
    fight(player, enemy, limit=1)

    assert player.treasures['SBB_TREASURE_PHOENIXFEATHER'][0].feather_used
    assert player.characters[2] is not None
    assert (player.characters[2].attack, player.characters[2].health) == (100, 4)
    assert (player.characters[7].attack, player.characters[7].health) == (1, 4)
