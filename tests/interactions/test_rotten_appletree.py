from sbbbattlesim import Board
from tests import make_character, make_player


def test_rotten_appletree():
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_ROTTENAPPLETREE', position=6, attack=0, health=5),
        ]
    )
    enemy = make_player(
        characters=[
            make_character(attack=1, health=1000, position=1),
        ]
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=2)


    assert board.p2.characters[1].health == 1


def test_rotten_appletree_support():
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_ROTTENAPPLETREE', position=1, attack=0, health=5),
        ]
    )
    enemy = make_player(
        characters=[
            make_character(attack=1, health=1000, position=1),
            make_character(id="SBB_CHARACTER_BABYROOT", attack=1, health=1000, position=5)
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=1)


    assert board.p2.characters[1].health == 1


def test_rotten_appletree_health_support_dies():
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_ROTTENAPPLETREE', position=1, attack=0, health=5),
            make_character(id='SBB_CHARACTER_BABYDRAGON', position=6, attack=3, health=3),
        ]
    )
    enemy = make_player(
        characters=[
            make_character(attack=1, health=1000, position=1),
            make_character(id="SBB_CHARACTER_BABYROOT", attack=1, health=1, position=5)
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    frontchar = board.p2.characters[1]
    backchar = board.p2.characters[5]
    board.p2.resolve_board()
    assert board.p2.characters[1].health == 1003
    winner, loser = board.fight(limit=2)


    assert backchar.dead
    assert frontchar.dead


def test_rotten_appletree_attack_support_dies():
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_ROTTENAPPLETREE', position=1, attack=0, health=5),
            make_character(id='SBB_CHARACTER_BABYDRAGON', position=5, attack=3, health=3),
        ]
    )
    enemy = make_player(
        characters=[
            make_character(attack=1, health=1000, position=1),
            make_character(id="SBB_CHARACTER_MADMADAMMIM", attack=1, health=1, position=5)
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    frontchar = board.p2.characters[1]
    backchar = board.p2.characters[5]
    board.p2.resolve_board()
    assert board.p2.characters[1].attack == 4

    winner, loser = board.fight(limit=2)


    assert frontchar.health == 1
    assert backchar.dead
