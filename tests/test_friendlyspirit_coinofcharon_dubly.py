from sbbbattlesim import Board
from tests import make_character, make_player
import pytest

@pytest.mark.parametrize('golden', (True, False))
def test_friendlyspirit_coinofcharon_dubly(golden):

    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_FRIENDLYGHOST', position=1, attack=5, health=5, golden=golden),
            make_character(id='SBB_CHARACTER_DUMBLEDWARF', position=5, attack=1, health=1, golden=golden),
        ],
        treasures=['''SBB_TREASURE_MONKEY'SPAW''']
    )
    enemy = make_player(
        characters=[make_character(attack=5, health=5)],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=None)

    if golden:
        final_stats = (55, 55)
    else:
        final_stats = (19, 19)

    assert (board.p1.characters[5].attack, board.p1.characters[5].health) == final_stats
