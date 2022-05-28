from sbbbattlesim import fight
from tests import make_character, make_player


def test_advanced_dubly_respawn():
    player = make_player(
        raw=True,
        characters=[
            make_character(id='SBB_CHARACTER_DUMBLEDWARF', position=1, attack=3, health=1),
        ],
        treasures=[
            'SBB_TREASURE_TREASURECHEST',
            "SBB_TREASURE_PHOENIXFEATHER",
            "SBB_TREASURE_WHIRLINGBLADES"
        ]
    )
    enemy = make_player(
        raw=True,
        characters=[make_character()],
    )
    fight(player, enemy)

    assert player.treasures['SBB_TREASURE_PHOENIXFEATHER'][0].feather_used

    assert (player.characters[1].attack, player.characters[1].health) == (3, 1)
    assert (player.characters[2].attack, player.characters[2].health) == (3, 1)


def test_advanced_respawn():
    player = make_player(
        raw=True,
        characters=[
            make_character(position=1, attack=3, health=1),
        ],
        treasures=[
            'SBB_TREASURE_TREASURECHEST',
            "SBB_TREASURE_PHOENIXFEATHER",
            "SBB_TREASURE_WHIRLINGBLADES"
        ]
    )
    enemy = make_player(
        raw=True,
        characters=[make_character()],
    )
    fight(player, enemy)

    assert player.treasures['SBB_TREASURE_PHOENIXFEATHER'][0].feather_used

    assert (player.characters[1].attack, player.characters[1].health) == (3, 1)
    assert (player.characters[2].attack, player.characters[2].health) == (3, 1)