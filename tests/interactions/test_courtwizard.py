import pytest

from sbbbattlesim import Board
from sbbbattlesim.utils import Tribe
from tests import make_character, make_player


@pytest.mark.parametrize('tribe', (Tribe.PRINCE, Tribe.PRINCESS, Tribe.DWARF))
def test_courtwizard(tribe):
    player = make_player(
        characters=[
            make_character(position=1),
            make_character(position=2)
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    enemy = make_player(
        characters=[
            make_character(position=1, tribes=[tribe]),
            make_character(id="SBB_CHARACTER_COURTWIZARD", position=5)
        ],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=1)
    board.p1.resolve_board()
    board.p2.resolve_board()

    if tribe in [Tribe.PRINCE, Tribe.PRINCESS]:
        assert board.p1.characters[1] is None and board.p1.characters[2] is None


def test_courtwizard_ranged():

    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_COURTWIZARD', position=6, attack=3, health=6),
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
