import pytest

from sbbbattlesim import Board
from tests import make_character, make_player


@pytest.mark.parametrize('golden', (True, False))
@pytest.mark.parametrize('summoner_id', ('SBB_CHARACTER_PRINCESSPEEP', 'SBB_CHARACTER_TWEEDLEDEE'))
def test_hippocampus(golden, summoner_id):
    player = make_player(
        characters=[
            make_character(id="SBB_CHARACTER_HUNGRYHUNGRYHIPPOCAMPUS",position=5, attack=1, health=1, golden=golden),
            make_character(id=summoner_id, position=1, attack=1, health=1),
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    enemy = make_player(
        characters=[make_character(attack=500, health=500)]
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=1)
    board.p1.resolve_board()
    board.p2.resolve_board()

    if summoner_id == 'SBB_CHARACTER_PRINCESSPEEP':
        if golden:
            final_stats = (1, 13)
        else:
            final_stats = (1, 7)
    else:
        final_stats = (1, 1)
        assert board.p1.characters[1] is not None  # there should be a tweedle dum there

    assert (board.p1.characters[5].attack, board.p1.characters[5].health) == final_stats


