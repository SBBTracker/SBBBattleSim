import pytest

from sbbbattlesim import fight
from sbbbattlesim.action import ActionReason
from sbbbattlesim.utils import Tribe
from tests import make_character, make_player


@pytest.mark.parametrize('attacker_golden', (True, False))
@pytest.mark.parametrize('defender_golden', (True, False))
def test_southern_siren(attacker_golden, defender_golden):
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_LOBO', position=1, attack=1, health=1, golden=attacker_golden),
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    enemy = make_player(
        characters=[make_character(attack=0, health=1, golden=defender_golden, tribes=[Tribe.DWARF])],
    )
    fight(player, enemy, limit=1)


    units_to_check = []
    units_to_check.append(player.characters[2])
    if attacker_golden:
        units_to_check.append(player.characters[3])

    for utc in units_to_check:
        assert utc is not None
        assert utc.golden is defender_golden
        assert utc.tribes == type(utc.tribes)([Tribe.DWARF])


def test_southern_siren_positioncheck():
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_LOBO', position=1, attack=1, health=1, golden=True),
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    enemy = make_player(
        characters=[make_character(attack=0, health=1)],
    )
    fight(player, enemy, limit=1)

    assert player.characters[2].position == 2
    assert player.characters[3].position == 3



def test_southern_siren_steal_shadowassassin_buff():
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_LOBO', position=1, attack=1, health=1),
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    enemy = make_player(
        characters=[make_character(id="SBB_CHARACTER_SHADOWASSASSIN", attack=0, health=1)],
    )
    fight(player, enemy, limit=1)

    assert player.characters[2].position == 2

    assert player.characters[2].attack == 1
    buffs = [r for r in player.characters[2]._action_history if r.reason == ActionReason.SHADOW_ASSASSIN_ON_SLAY_BUFF]

    assert len(buffs) == 1
    assert sum([b.attack for b in buffs]) == 1
    assert sum([b.health for b in buffs]) == 0
    