from sbbbattlesim import Board
from tests import make_character, make_player
import pytest

def test_soltak():
    player = make_player(
        characters=[
            make_character(id="SBB_CHARACTER_SOLTAKANCIENT", position=2, attack=0, health=20),
            make_character(position=5, attack=1, health=1),
        ]
    )
    enemy = make_player(
        characters=[make_character(id="SBB_CHARACTER_BABYDRAGON", attack=1, health=1)],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=1)
    board.p1.resolve_board()
    board.p2.resolve_board()

    assert board.p1.characters[5] is not None
    assert board.p2.characters[1] is None

