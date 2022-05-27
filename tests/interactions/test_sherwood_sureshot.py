from sbbbattlesim import fight
from tests import make_character, make_player


def test_sureshot_ranged():
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_FOXTAILARCHER', position=6, attack=3, health=6),
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    enemy = make_player(
        characters=[make_character(attack=1, health=1)],
    )
    fight(player, enemy, limit=2)


    assert (player.characters[6].attack, player.characters[6].health) == (3, 6)
