import pytest

from sbbbattlesim import Board
from sbbbattlesim.utils import StatChangeCause
from tests import make_character, make_player


@pytest.mark.parametrize('golden', (True, False))
@pytest.mark.parametrize('level', (2, 3, 4, 5, 6))
@pytest.mark.parametrize('repeat', range(30))
def test_wombat_dying(golden, level, repeat):
    player = make_player(
        level=level,
        characters=[
            make_character(id='SBB_CHARACTER_WOMBATSINDISGUISE', attack=2, health=3, position=1, golden=golden),
        ],
    )
    enemy = make_player(
        characters=[make_character(attack=5, health=5)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=1)
    board.p1.resolve_board()
    board.p2.resolve_board()

    summoned_char = board.p1.characters[1]

    assert summoned_char is not None
    assert 1 < summoned_char._level <= level
    assert summoned_char.golden == golden

    wombat_buffs = [
        r for r in board.p1.characters[1].stat_history if r.reason == StatChangeCause.WOMBATS_IN_DISGUISE_BUFF
    ]

    assert len(wombat_buffs) == 1
