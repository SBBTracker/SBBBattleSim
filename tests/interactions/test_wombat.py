import pytest

from sbbbattlesim import fight
from sbbbattlesim.action import ActionReason
from sbbbattlesim.utils import Tribe
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
    fight(player, enemy, limit=1)


    summoned_char = player.characters[1]

    assert summoned_char is not None
    assert 1 < summoned_char._level <= level
    assert summoned_char.golden == golden

    wombat_buffs = [
        r for r in player.characters[1]._action_history if r.reason == ActionReason.WOMBATS_IN_DISGUISE_BUFF
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
    fight(player, enemy, limit=1)


    summoned_char = player.characters[1]

    assert summoned_char is not None

    wombat_buff = None
    for action in player.characters[1]._action_history:
        if action.reason == ActionReason.WOMBATS_IN_DISGUISE_BUFF:
            wombat_buff = action
            break

    assert wombat_buff
    assert wombat_buff.attack, wombat_buff.health == (2, 3)


@pytest.mark.parametrize('repeat', range(30))
def test_bearstain_wombat_phoenix(repeat):
    '''This is an interesting one -- The 1st unit comes back from Phoenix Feather, the 2nd and 3rd are Reduplicators, and the 4th is a copy of the 1st and gets buffed again with the same buffs the 1st received'''
    player = make_player(
        level=2,
        raw=True,
        characters=[
            make_character(id='SBB_CHARACTER_WOMBATSINDISGUISE', position=1, attack=30, health=26, golden=True, tribes=[Tribe.ANIMAL]),
            make_character(id='SBB_CHARACTER_PROSPERO', position=5, golden=False),
            make_character(id='SBB_CHARACTER_PROSPERO', position=6, golden=True),
            make_character(position=7)
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
    original_wombat = player.characters[1]

    fight(player, enemy, limit=1)

    assert player.characters[1] is original_wombat
    assert original_wombat._base_attack == 120, original_wombat.pretty_print()
    assert original_wombat._base_health == 104, original_wombat.pretty_print()

    wombat2 = player.characters[2]
    assert wombat2._base_attack == 120
    assert wombat2._base_health == 104

    wombat3 = player.characters[3]
    assert wombat3._base_attack == 120
    assert wombat3._base_health == 104

    wombat4 = player.characters[4]
    assert wombat4._base_attack == 210
    assert wombat4._base_health == 182

    char5 = player.characters[5]
    assert char5 is not None


