import pytest

from sbbbattlesim import Board
from sbbbattlesim.utils import Tribe
from tests import make_character, make_player


@pytest.mark.parametrize('has_wight', (True, False))
@pytest.mark.parametrize('golden', (True, False))
def test_lordy(has_wight, golden):
    player = make_player(
        characters=[
            make_character(
                id="SBB_CHARACTER_FORGEMASTERDWARF",position=1, attack=1, health=1, tribes=[Tribe.DWARF], golden=golden
            ),
            make_character(position=6, attack=1, health=1, tribes=[Tribe.DWARF]),
            make_character(position=5, attack=1, health=1),
            make_character(position=2, attack=1, health=1, id="SBB_CHARACTER_PRINCESSNIGHT" if has_wight else "foo")
        ],
    )
    enemy = make_player()

    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=0)
    board.p1.resolve_board()
    board.p2.resolve_board()

    if has_wight:
        if golden:
            final_stats = (13, 13)
        else:
            final_stats = (7, 7)
    else:
        if golden:
            final_stats = (9, 9)
        else:
            final_stats = (5, 5)

    d1stats = (board.p1.characters[1].attack, board.p1.characters[1].health)
    d6stats = (board.p1.characters[6].attack, board.p1.characters[6].health)
    not_d5stats = (board.p1.characters[5].attack, board.p1.characters[5].health)
    if has_wight:
        wightstats = board.p1.characters[2].attack, board.p1.characters[2].health
        assert wightstats == final_stats

    assert d1stats == final_stats
    assert d6stats == final_stats
    assert not_d5stats == (1, 1)
