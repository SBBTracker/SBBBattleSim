from sbbbattlesim import Board
from sbbbattlesim.utils import Tribe
from tests import make_character, make_player


def test_echowood_queenofhearts():
    player = make_player(
        hero = "SBB_HERO_MUERTE",
        characters=[
            make_character(id="SBB_CHARACTER_BLACKCAT",position=2, attack=1, health=1, tribes=[Tribe.EVIL]),
            make_character(id="SBB_CHARACTER_ECHOWOODSHAMBLER",position=5, attack=1, health=1),
            make_character(id="SBB_CHARACTER_QUEENOFHEARTS", position=6, attack=1, health=1),
            make_character(id="SBB_CHARACTER_ECHOWOODSHAMBLER", position=7, attack=1, health=1, golden=True),
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    enemy = make_player(
        characters=[
            make_character(health=2)
        ],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=2)
    board.p1.resolve_board()
    board.p2.resolve_board()

    golden_final_stats = (9, 9)

    final_stats = (5, 5)

    assert (board.p1.characters[5].attack, board.p1.characters[5].health) == final_stats
    assert (board.p1.characters[7].attack, board.p1.characters[7].health) == golden_final_stats


def test_echowood_supported_token():
    player = make_player(
        # hero = "SBB_HERO_MUERTE",
        characters=[
            make_character(id="SBB_CHARACTER_BLACKCAT", position=2, attack=1, health=1, tribes=[Tribe.EVIL]),
            make_character(id="SBB_CHARACTER_BABYROOT", position=5, attack=0, health=1),
            make_character(id="SBB_CHARACTER_ECHOWOODSHAMBLER", position=7, attack=1, health=1),
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    enemy = make_player(
        characters=[
            make_character(attack=10, health=2)
        ],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=2)
    board.p1.resolve_board()
    board.p2.resolve_board()

    assert (board.p1.characters[7].attack, board.p1.characters[7].health) == (1, 4)


def test_bearstain_echowood():

    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_PROSPERO', position=5),
            make_character(id='SBB_CHARACTER_BLACKCAT', position=1),
            make_character(id="SBB_CHARACTER_ECHOWOODSHAMBLER", position=7, attack=1, health=1),
        ],
    )
    enemy = make_player(
        characters=[make_character(attack=500, health=500)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=1)
    board.p1.resolve_board()
    board.p2.resolve_board()

    assert board.p1.characters[7].attack, board.p1.characters[7].health == (6, 6)

def test_echowood_evil_queen():

    player = make_player(
        hero = "SBB_HERO_MUERTE",
        characters=[
            make_character(id="SBB_CHARACTER_BLACKCAT",position=2, attack=1, health=1, tribes=[Tribe.EVIL]),
            make_character(id="SBB_CHARACTER_QUEENOFHEARTS", position=6, attack=1, health=1),
            make_character(id="SBB_CHARACTER_ECHOWOODSHAMBLER", position=7, attack=1, health=1),
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    enemy = make_player(
        characters=[
            make_character(health=3)
        ],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=2)
    board.p1.resolve_board()
    board.p2.resolve_board()

    assert (board.p1.characters[7].attack, board.p1.characters[7].health) == (5, 5)


def test_echowood_pumpkin():

    player = make_player(
        characters=[
            make_character(id="SBB_CHARACTER_PUMPKINKING",position=2, attack=1, health=1, tribes=[Tribe.EVIL]),
            make_character(id="SBB_CHARACTER_ECHOWOODSHAMBLER", position=7, attack=1, health=1),
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS''',
            "SBB_TREASURE_SUMMONINGCIRCLE"
        ]
    )
    enemy = make_player(
        characters=[
            make_character(health=3)
        ],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=1)
    board.p1.resolve_board()
    board.p2.resolve_board()

    assert (board.p1.characters[7].attack, board.p1.characters[7].health) == (2, 2)


def test_echowood_pumpkin_support():

    player = make_player(
        characters=[
            make_character(id="SBB_CHARACTER_PUMPKINKING",position=2, attack=1, health=1, tribes=[Tribe.EVIL]),
            make_character(id="SBB_CHARACTER_ECHOWOODSHAMBLER", position=7, attack=1, health=1),
            make_character(id="SBB_CHARACTER_BABYROOT", position=5, attack=0, health=3)
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS''',
        ]
    )
    enemy = make_player(
        characters=[
            make_character(attack=int(1e100), health=3)
        ],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=1)
    board.p1.resolve_board()
    board.p2.resolve_board()

    assert (board.p1.characters[7].attack, board.p1.characters[7].health) == (1, 4)


def test_echowood_romeo():
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_ROMEO', position=2, attack=1, health=1),
            make_character(id='SBB_CHARACTER_JULIET', attack=7, health=7, position=1),
            make_character(id="SBB_CHARACTER_ECHOWOODSHAMBLER", position=7, attack=1, health=1),
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    enemy = make_player(
        characters=[make_character(attack=7, health=8)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    juliet = board.p1.characters[2]
    winner, loser = board.fight(limit=2)
    board.p1.resolve_board()
    board.p2.resolve_board()

    assert (board.p1.characters[7].attack, board.p1.characters[7].health) == (8, 8)

# TODO test echowood with storm king, puff puff, and crafty emerging from some spawning mechanic


