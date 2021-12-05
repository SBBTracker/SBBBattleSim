from sbbbattlesim import Board
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
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=0)
    board.p1.resolve_board()
    board.p2.resolve_board()


    assert (board.p1.characters[1].attack, board.p1.characters[1].health) == (431, 191)
