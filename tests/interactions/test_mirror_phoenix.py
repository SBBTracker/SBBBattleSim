from sbbbattlesim import fight
from tests import make_character, make_player


def test_mirror_phoenixfeather():
    player = make_player(
        characters=[
            make_character(position=1, attack=10, health=10),
        ],
        treasures=[
            'SBB_TREASURE_PHOENIXFEATHER',
            'SBB_TREASURE_MIRRORUNIVERSE'
        ]
    )
    enemy = make_player(
        characters=[make_character(attack=100, health=100)],
    )
    fight(player, enemy, limit=-1)


    assert enemy.characters[1].health == 78
