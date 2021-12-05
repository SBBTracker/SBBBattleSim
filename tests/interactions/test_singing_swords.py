import pytest

from sbbbattlesim import Board
from tests import make_character, make_player


@pytest.mark.parametrize('golden', (True, False))
@pytest.mark.parametrize('mimic', (True, False))
def test_madmim_singingswords(golden, mimic):

    if golden:
        if mimic:
            final_stats = 21
        else:
            final_stats = 14
    else:
        if mimic:
            final_stats = 12
        else:
            final_stats = 8

    player = make_player(
        characters=[
            make_character(id="SBB_CHARACTER_MADMADAMMIM",position=5, attack=1, health=1, golden=golden),
            make_character(position=1, attack=1, health=1),
        ],
        treasures=[
            "SBB_TREASURE_WHIRLINGBLADES",
            "SBB_TREASURE_TREASURECHEST" if mimic else "",
        ]
    )
    enemy = make_player(
        characters=[
            make_character(id="SBB_CHARACTER_BABYDRAGON", position=5, attack=1, health=1),
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS''',
        ]
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=1)
    board.p1.resolve_board()
    board.p2.resolve_board()


    assert (board.p1.characters[1].attack, board.p1.characters[1].health) == (1, 1)



def test_singingswords_bearstain():
    player = make_player(
        characters=[
            make_character(id="SBB_CHARACTER_PROSPERO",position=5, attack=1, health=1),
            make_character(id="SBB_CHARACTER_BLACKCAT",position=1, attack=1, health=1),
        ],
        treasures=[
            "SBB_TREASURE_WHIRLINGBLADES"
        ]
    )
    enemy = make_player(
        characters=[
            make_character(position=5, attack=5, health=5),
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS''',
        ]
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=1)
    board.p1.resolve_board()
    board.p2.resolve_board()

    assert (board.p1.characters[1].attack, board.p1.characters[1].health) == (18, 6)

def test_singingswords_bearstain_unassumingsheep():
    player = make_player(
        characters=[
            make_character(id="SBB_CHARACTER_PROSPERO",position=5, attack=1, health=1),
            make_character(id="SBB_CHARACTER_UNASSUMINGSHEEP",position=1, attack=1, health=1),
        ],
        treasures=[
            "SBB_TREASURE_WHIRLINGBLADES",
            "SBB_TREASURE_TREASURECHEST",
        ]
    )
    enemy = make_player(
        characters=[
            make_character(position=5, attack=5, health=5),
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS''',
        ]
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=1)
    board.p1.resolve_board()
    board.p2.resolve_board()

    assert (board.p1.characters[1].attack, board.p1.characters[1].health) == (96, 16)

def test_singingswords_dos_bearstain():
    player = make_player(
        characters=[
            make_character(id="SBB_CHARACTER_PROSPERO",position=5, attack=1, health=1),
            make_character(id="SBB_CHARACTER_PROSPERO", position=6, attack=1, health=1),
            make_character(id="SBB_CHARACTER_BLACKCAT",position=1, attack=1, health=1),
        ],
        treasures=[
            "SBB_TREASURE_WHIRLINGBLADES"
        ]
    )
    enemy = make_player(
        characters=[
            make_character(position=5, attack=1, health=1),
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS''',
        ]
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=1)
    board.p1.resolve_board()
    board.p2.resolve_board()

    assert (board.p1.characters[1].attack, board.p1.characters[1].health) == (50, 15)


def test_singingswords_mimic_roundtable():

    player = make_player(
        characters=[
            make_character(position=1, attack=21, health=30),
        ],
        treasures=[
            "SBB_TREASURE_TREASURECHEST",
            "SBB_TREASURE_THEROUNDTABLE",
            "SBB_TREASURE_WHIRLINGBLADES"
        ]
    )
    enemy = make_player()
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=0)
    board.p1.resolve_board()
    board.p2.resolve_board()


    assert (board.p1.characters[1].attack, board.p1.characters[1].health) == (48, 48)

    player = make_player(
        characters=[
            make_character(position=1, attack=0, health=3),
        ],
        treasures=[
            "SBB_TREASURE_TREASURECHEST",
            "SBB_TREASURE_THEROUNDTABLE",
            "SBB_TREASURE_WHIRLINGBLADES"
        ]
    )
    enemy = make_player()
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=0)
    board.p1.resolve_board()
    board.p2.resolve_board()


    assert (board.p1.characters[1].attack, board.p1.characters[1].health) == (9, 9)



def test_backline_blackcat():
    player = make_player(
        characters=[
            make_character(id="SBB_CHARACTER_BLACKCAT",position=5, attack=1, health=1),
        ],
        treasures=[
            "SBB_TREASURE_WHIRLINGBLADES"
        ]
    )
    enemy = make_player(
        characters=[
            make_character(position=5, attack=1, health=1),
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS''',
        ]
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=1)
    board.p1.resolve_board()
    board.p2.resolve_board()

    assert (board.p1.characters[5].attack, board.p1.characters[5].health) == (1, 1)

def test_multiple_echowoods():
    player = make_player(
        characters=[
            make_character(id="SBB_CHARACTER_ECHOWOODSHAMBLER", position=2, attack=2, health=1),
            make_character(id="SBB_CHARACTER_ECHOWOODSHAMBLER", position=3, attack=2, health=1),
            make_character(id="SBB_CHARACTER_BLACKCAT", position=1, attack=2, health=1),
        ],
        treasures=[
            "SBB_TREASURE_WHIRLINGBLADES",
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    enemy = make_player(
        characters=[
            make_character(position=5, attack=1, health=1),
        ]
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=1)
    board.p1.resolve_board()
    board.p2.resolve_board()

    assert (board.p1.characters[2].attack, board.p1.characters[2].health) == (4, 1)