import pytest

from sbbbattlesim import Board
from sbbbattlesim.utils import Tribe
from tests import make_character, make_player

@pytest.mark.parametrize('r', range(30))
@pytest.mark.parametrize('golden', (True, False))
@pytest.mark.parametrize('limit', (1, 2, 4))
def test_fairy_godmother(golden, limit, r):
    player = make_player(
        characters=[
            make_character(
                id="SBB_CHARACTER_FAIRYGODMOTHER", position=5, attack=1, health=1,
                golden=golden, tribes=[Tribe.GOOD]
            ),
            make_character(
                id="SBB_CHARACTER_PRINCESSPEEP", position=1, attack=1, health=1,
                tribes=[Tribe.GOOD]
            ),
        ],
    )
    enemy = make_player(
        treasures=['''SBB_TREASURE_HERMES'BOOTS'''],
        characters=[make_character(attack=500, health=500)]
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=limit)


    fairy_stats = (board.p1.characters[5].attack, board.p1.characters[5].health)

    if limit == 1:
        assert fairy_stats == (1, 5) if golden else (1, 3)
    if limit == 2:
        health = 9 if golden else 5
        assert fairy_stats == (1, 9) if golden else (1, 5)
        assert board.p1.characters[2].health == health, board.p1.characters[2].health
    if limit == 4:
        assert fairy_stats == (1, 17) if golden else (1, 9)
