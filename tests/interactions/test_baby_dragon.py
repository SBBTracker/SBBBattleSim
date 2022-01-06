from sbbbattlesim import Board
from tests import make_character, make_player


def test_baby_dragon():
    player = make_player(
        raw=True,
        characters=[
            make_character(id='SBB_CHARACTER_BABYDRAGON', position=6, attack=3, health=3),
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    enemy = make_player(
        raw=True,
        characters=[make_character(attack=1, health=1, position=1),
                    make_character(attack=2, health=2, position=5)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=1)


    assert (board.p1.characters[6].attack, board.p1.characters[6].health) == (3, 1)
    assert board.p2.characters[1] is not None
    assert board.p2.characters[5] is None
