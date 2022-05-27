from sbbbattlesim import fight
from tests import make_character, make_player


def test_cupid_effect():
    player = make_player(
        raw=True,
        characters=[
            make_character(id="SBB_CHARACTER_CUPID", position=1),
            make_character(position=2)
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    enemy = make_player(
        characters=[
            make_character(position=1),
            make_character(position=5, health=2)
        ],
    )
    fight(player, enemy, limit=1)

    assert enemy.characters[5] is None
    assert enemy.characters[1] is None


def test_cupid_ranged():
    player = make_player(
        raw=True,
        characters=[
            make_character(id='SBB_CHARACTER_CUPID', position=6, attack=3, health=6),
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
