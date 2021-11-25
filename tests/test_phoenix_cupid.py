from sbbbattlesim import Board
from tests import make_character, make_player


def test_phoenix_cupid():

    player = make_player(
        characters=[
            make_character(position=1, attack=1, health=500),
            make_character(position=5, attack=500, health=1),
        ],
        treasures=['SBB_TREASURE_PHOENIXFEATHER']
    )
    enemy = make_player(
        characters=[make_character(id="SBB_CHARACTER_CUPID", attack=1, health=1)],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=1)

    assert board.p1.characters[1] is None
    assert board.p1.characters[5] is None

