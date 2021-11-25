from sbbbattlesim import Board
from tests import make_character, make_player
import pytest

@pytest.mark.parametrize('golden', (True, False))
@pytest.mark.parametrize('mimic', (True, False))
@pytest.mark.parametrize('evil_eye', (True, False))
def test_advanced_slay(golden, mimic, evil_eye):

    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_RIVERWISHMERMAID', position=5, attack=5, health=5, golden=False),
            make_character(id='SBB_CHARACTER_BABAYAGA', position=6, attack=3, health=6, golden=golden),
            make_character(position=2),
            make_character(id="SBB_CHARACTER_SHADOWASSASSIN", position=7)
        ],
        treasures= [
            'SBB_TREASURE_HELMOFCOMMAND' if evil_eye else '',
            'SBB_TREASURE_TREASURECHEST' if mimic else '',
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    enemy = make_player(
        characters=[make_character(attack=0, health=1)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=1)

    yaga_multiplier = 2 if golden else 1
    evil_eye_additor = yaga_multiplier if evil_eye else 0
    mimic_multiplier = 2 if mimic else 1

    slay_count = 1 + yaga_multiplier + evil_eye_additor * mimic_multiplier

    final_stat = 1 + slay_count*(3 if mimic and evil_eye else 2 if evil_eye else 1)
    final_stats = (final_stat, final_stat)

    assert (board.p1.characters[2].attack, board.p1.characters[2].health) == final_stats
    assert (board.p1.characters[7].attack, board.p1.characters[7].health) == final_stats
