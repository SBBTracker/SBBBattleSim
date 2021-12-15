import pytest

from sbbbattlesim import Board
from sbbbattlesim.utils import Tribe
from tests import make_character, make_player


@pytest.mark.parametrize('golden', (True, False))
def test_lordy(golden):
    player = make_player(
        characters=[
            make_character(
                id="SBB_CHARACTER_FORGEMASTERDWARF", position=1, attack=1, health=1, tribes=[Tribe.DWARF], golden=golden
            ),
            make_character(position=6, attack=1, health=1, tribes=[Tribe.DWARF]),
            make_character(position=5, attack=1, health=1),
        ],
    )
    enemy = make_player()

    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=0)
    board.p1.resolve_board()
    board.p2.resolve_board()


    if golden:
        final_stats = (9, 9)
    else:
        final_stats = (5, 5)

    d1stats = (board.p1.characters[1].attack, board.p1.characters[1].health)
    d6stats = (board.p1.characters[6].attack, board.p1.characters[6].health)
    not_d5stats = (board.p1.characters[5].attack, board.p1.characters[5].health)

    assert d1stats == final_stats
    assert d6stats == final_stats
    assert not_d5stats == (1, 1)
