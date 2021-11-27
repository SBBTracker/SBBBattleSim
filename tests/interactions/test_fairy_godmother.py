from sbbbattlesim import Board
from tests import make_character, make_player
from sbbbattlesim.utils import Tribe
import pytest

@pytest.mark.parametrize('golden', (True, False))
@pytest.mark.parametrize('limit', (1, 2, 4))
def test_fairy_godmother(golden, limit):
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
    board.p1.resolve_board()
    board.p2.resolve_board()

    fairy_stats = (board.p1.characters[5].attack, board.p1.characters[5].health)

    if limit == 1:
        assert fairy_stats == (1, 5) if golden else (1, 3)
    if limit == 2:
        assert fairy_stats == (1, 9) if golden else (1, 5)
        assert board.p1.characters[2].health == 9 if golden else 5
    if limit == 4:
        assert fairy_stats == (1, 17) if golden else (1, 9)
