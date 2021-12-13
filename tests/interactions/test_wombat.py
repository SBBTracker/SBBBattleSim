import pytest

from sbbbattlesim import Board
from sbbbattlesim.utils import StatChangeCause, Tribe
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
        r for r in board.p1.characters[1]._action_history if r.reason == StatChangeCause.WOMBATS_IN_DISGUISE_BUFF
    ]

    assert len(wombat_buffs) == 1


def test_charon_wombat():
    '''Wombat death does not get buffed by coin of charon for some reason'''
    player = make_player(
        level=2,
        characters=[
            make_character(id='SBB_CHARACTER_WOMBATSINDISGUISE', attack=2, health=3, position=1),
        ],
        treasures=[
            '''SBB_TREASURE_MONKEY'SPAW'''
        ]
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

    stat_history = board.p1.characters[1]._action_history[0]

    assert stat_history.attack, stat_history.health == (2, 3)


def test_bearstain_wombat_phoenix():
    '''This is an interesting one -- The 1st unit comes back from Phoenix Feather, the 2nd and 3rd are Reduplicators, and the 4th is a copy of the 1st and gets buffed again with the same buffs the 1st received'''
    player = make_player(
        level=2,
        raw=True,
        characters=[
            make_character(id='SBB_CHARACTER_WOMBATSINDISGUISE', position=1, attack=30, health=26, golden=True, tribes=[Tribe.ANIMAL]),
            make_character(id='SBB_CHARACTER_PROSPERO', position=6, golden=False),
            make_character(id='SBB_CHARACTER_PROSPERO', position=7, golden=True),
        ],
        treasures=[
            "SBB_TREASURE_PHOENIXFEATHER",
            "SBB_TREASURE_TREASURECHEST",
            "SBB_TREASURE_REDUPLICATOR"
        ]
    )
    enemy = make_player(
        characters=[make_character(attack=500, health=500)],
    )
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    original_wombat = board.p1.characters[1]

    winner, loser = board.fight(limit=1)
    board.p1.resolve_board()
    board.p2.resolve_board()

    assert board.p1.characters[1] is original_wombat
    assert original_wombat._base_attack == 114
    assert original_wombat._base_health == 98

    wombat2 = board.p1.characters[2]
    assert wombat2._base_attack == 114
    assert wombat2._base_health == 98

    wombat3 = board.p1.characters[3]
    assert wombat3._base_attack == 114
    assert wombat3._base_health == 98

    wombat4 = board.p1.characters[4]
    assert wombat4._base_attack == 204
    assert wombat4._base_health == 176

    char5 = board.p1.characters[5]
    assert char5 is not None


