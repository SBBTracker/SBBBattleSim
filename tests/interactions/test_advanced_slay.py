import pytest

from sbbbattlesim import Board
from tests import make_character, make_player


@pytest.mark.parametrize('golden', (True, False))
@pytest.mark.parametrize('mimic', (True, False))
@pytest.mark.parametrize('evil_eye', (True, False))
def test_riverwish_yaga(golden, mimic, evil_eye):
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_RIVERWISHMERMAID', position=5, attack=5, health=5, golden=False),
            make_character(id='SBB_CHARACTER_BABAYAGA', position=6, attack=3, health=6, golden=golden),
            make_character(position=2),
            make_character(id="SBB_CHARACTER_SHADOWASSASSIN", position=7, attack= 1, health=1)
        ],
        treasures=[
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
    board.p1.resolve_board()
    board.p2.resolve_board()

    yaga_multiplier = 2 if golden else 1
    evil_eye_additor = yaga_multiplier if evil_eye else 0
    mimic_multiplier = 2 if mimic else 1

    slay_multiplyer = 1 + yaga_multiplier + evil_eye_additor * mimic_multiplier
    slay_count = 1
    if mimic and evil_eye:
        slay_count = 3
    elif evil_eye:
        slay_count = 2

    final_stat = 1 + slay_count * slay_multiplyer
    final_stats = (final_stat, final_stat)

    assert (board.p1.characters[2].attack, board.p1.characters[2].health) == final_stats
    assert (board.p1.characters[7].attack, board.p1.characters[7].health) == (final_stat, 1)


@pytest.mark.parametrize('mimic', (True, False))
@pytest.mark.parametrize('evil_eye', (True, False))
def test_double_yaga(mimic, evil_eye):
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_BABAYAGA', position=5, attack=5, health=5, golden=False),
            make_character(id='SBB_CHARACTER_BABAYAGA', position=6, attack=3, health=6, golden=False),
            make_character(id='SBB_CHARACTER_CATBURGLAR', position=2, attack=1, health=1),
            make_character(id="SBB_CHARACTER_SHADOWASSASSIN", position=7, attack=1, health=1)
        ],
        treasures=[
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
    board.p1.resolve_board()
    board.p2.resolve_board()

    evil_eye_additor = 1 if evil_eye else 0
    mimic_multiplier = 2 if mimic else 1

    slay_multiplyer = 1 + evil_eye_additor * mimic_multiplier
    slay_count = 1

    final_stat = 1 + 1 + slay_count * slay_multiplyer * 2
    final_stats = (final_stat, final_stat)

    assert (board.p1.characters[7].attack, board.p1.characters[7].health) == (final_stat, 1)
