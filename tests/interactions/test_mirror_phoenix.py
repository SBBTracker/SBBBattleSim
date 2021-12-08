from sbbbattlesim import Board
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
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=-1)
    board.p1.resolve_board()
    board.p2.resolve_board()

    assert board.p2.characters[1].health == 78
