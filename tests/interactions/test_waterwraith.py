import pytest

from sbbbattlesim import Board
from tests import make_character, make_player
from sbbbattlesim.events import OnDamagedAndSurvived
from sbbbattlesim.utils import Tribe
from sbbbattlesim.characters import registry as character_registry


@pytest.mark.parametrize('golden', (True, False))
@pytest.mark.parametrize('on', (True, False))
def test_wraith(golden, on):
    p = 2 if on else 3
    player = make_player(
        characters=[
            make_character(id="SBB_CHARACTER_WATERWRAITH", position=p, attack=1, health=1, golden=golden),
            make_character(position=1, attack=1, health=1),
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    enemy = make_player(
        characters=[make_character(attack=500, health=500)]
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=1)


    if not on:
        final_stats = (1, 1)
    elif golden:
        final_stats = (3, 3)
    else:
        final_stats = (2, 2)

    assert (board.p1.characters[p].attack, board.p1.characters[p].health) == final_stats


