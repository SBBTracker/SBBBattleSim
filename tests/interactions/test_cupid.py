from sbbbattlesim import Board
from tests import make_character, make_player


def test_cupid_effect():
    player = make_player(
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
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=1)
    board.p1.resolve_board()
    board.p2.resolve_board()

    assert board.p2.characters[5] is None
    assert board.p2.characters[1] is None


def test_cupid_ranged():

    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_CUPID', position=6, attack=3, health=6),
        ],
        treasures= [
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    enemy = make_player(
        characters=[make_character(attack=1, health=1)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=2)
    board.p1.resolve_board()
    board.p2.resolve_board()

    assert (board.p1.characters[6].attack, board.p1.characters[6].health) == (3, 6)
