from tests import make_character, make_player


def test_lightning_dragon():
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_LIGHTNINGDRAGON', position=6, attack=1, health=1),
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    enemy = make_player(
        characters=[
            make_character(attack=1, health=1, position=1),
            make_character(attack=1, health=1, position=5)
        ],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    dragon = player.characters[6]
    frontline = enemy.characters[1]
    backline = enemy.characters[5]

    winner, loser = board.fight(limit=0)


    assert dragon.dead
    assert not frontline.dead
    assert backline.dead
