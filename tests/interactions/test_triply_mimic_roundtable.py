from sbbbattlesim import fight
from tests import make_character, make_player


def test_mimic_triply_roundtable():
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_DUMBLEDWARF', position=1, attack=71, health=11, golden=True),
        ],
        treasures=[
            "SBB_TREASURE_TREASURECHEST",
            "SBB_TREASURE_THEROUNDTABLE"
        ]
    )
    enemy = make_player()
    fight(player, enemy, limit=0)


    assert (player.characters[1].attack, player.characters[1].health) == (431, 191)
