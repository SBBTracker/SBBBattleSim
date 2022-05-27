from sbbbattlesim import fight
from tests import make_character, make_player


def test_mittens_phoenixfeather():
    player = make_player(
        characters=[
            make_character(position=1, attack=500, health=1),
            make_character(position=5, attack=1, health=1),
        ],
        treasures=['SBB_TREASURE_PHOENIXFEATHER']
    )
    enemy = make_player(
        characters=[make_character(attack=1, health=1)],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''', "SBB_TREASURE_EXPLODINGMITTENS"]
    )
    fight(player, enemy, limit=-1)


    assert player.characters[1] is None
    assert player.characters[5] is not None and player.characters[5].attack == 1


