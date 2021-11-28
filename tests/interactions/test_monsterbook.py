from sbbbattlesim import Board
from tests import make_character, make_player
import pytest
from sbbbattlesim.utils import StatChangeCause

@pytest.mark.parametrize('golden', (True, False))
def test_monsterbook(golden):

    player = make_player(
        level=2,
        characters=[
            make_character(id='SBB_CHARACTER_MONSTERBOOK', position=1, attack=1, health=1, golden=golden),
            make_character(id='SBB_CHARACTER_WIZARD', position=2, attack=1, health=2)
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    enemy = make_player(
        characters=[make_character(attack=1, health=1)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=1)
    board.p1.resolve_board()
    board.p2.resolve_board()

    wizardbuffs = [
        r for r in board.p1.characters[2].stat_history if r.reason == StatChangeCause.WIZARDS_FAMILIAR
    ]

    assert len(wizardbuffs) == (2 if golden else 1)

