from sbbbattlesim import Board
from tests import make_character, make_player


def test_negative_attack():
    player = make_player(
        characters=[
            make_character(),
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    enemy = make_player(
        characters=[
            make_character(attack=-100)
        ],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=1)


    assert (board.p1.characters[1].attack, board.p1.characters[1].health) == (1, 1)
