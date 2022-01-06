import pytest

from sbbbattlesim import Board
from tests import make_character, make_player


@pytest.mark.parametrize('golden', (True, False))
def test_chup(golden):
    player = make_player(
        raw=True,
        characters=[
            make_character(id="SBB_CHARACTER_THECHUPACABRA", position=2, attack=1, health=1, golden=golden),
            make_character(position=5, attack=1, health=1),
            make_character(position=6, attack=1, health=1),
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    enemy = make_player(
        raw=True,
        characters=[make_character(attack=0, health=1)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=1)


    final_stats = (5, 1) if golden else (3, 1)

    for i in [2, 5, 6]:
        assert (board.p1.characters[i].attack, board.p1.characters[i].health) == final_stats
