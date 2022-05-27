from sbbbattlesim import fight
from tests import make_character, make_player


def test_mittens_smallblackcat():
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_BLACKCAT', position=1, attack=1, health=1),
        ]
    )
    enemy = make_player(
        characters=[make_character(attack=1, health=1)],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''', "SBB_TREASURE_EXPLODINGMITTENS"]
    )
    fight(player, enemy, limit=-1)


    assert player.characters[1].id == 'SBB_CHARACTER_CAT'


def test_mimic_mittens_smallblackcat():
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_BLACKCAT', position=1, attack=1, health=1),
        ]
    )
    enemy = make_player(
        characters=[make_character(attack=1, health=1)],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''', "SBB_TREASURE_EXPLODINGMITTENS", "SBB_TREASURE_TREASURECHEST"]
    )
    fight(player, enemy, limit=-1)


    assert player.characters[1].id == 'SBB_CHARACTER_CAT'


def test_mimic_mittens_bigblackcat():
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_BLACKCAT', position=1, attack=2, health=2),
        ]
    )
    enemy = make_player(
        characters=[make_character(attack=1, health=1)],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''', "SBB_TREASURE_EXPLODINGMITTENS", "SBB_TREASURE_TREASURECHEST"]
    )
    fight(player, enemy, limit=-1)


    assert player.characters[1] is None
