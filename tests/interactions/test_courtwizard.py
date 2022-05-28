import pytest

from sbbbattlesim import fight
from sbbbattlesim.action import ActionReason
from sbbbattlesim.events import OnDeath
from sbbbattlesim.utils import Tribe
from tests import make_character, make_player


@pytest.mark.parametrize('tribe', (Tribe.ROYAL, Tribe.DWARF))
def test_courtwizard(tribe):
    player = make_player(
        raw=True,
        characters=[
            make_character(position=1),
            make_character(position=2)
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    enemy = make_player(
        raw=True,
        characters=[
            make_character(attack=10, position=1, tribes=[tribe]),
            make_character(id="SBB_CHARACTER_COURTWIZARD", position=5)
        ],
    )
    fight(player, enemy, limit=1)

    if tribe in [Tribe.ROYAL, Tribe.ROYAL]:
        assert player.characters[1] is None and player.characters[2] is None


def test_courtwizard_diesandproccs():
    '''If court wizard dies and procs, no error should thrown and it should not attack'''
    player = make_player(
        raw=True,
        characters=[
            make_character(id="SBB_CHARACTER_WRETCHEDMUMMY", position=1),
            make_character(position=2)
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    enemy = make_player(
        raw=True,
        characters=[
            make_character(position=1, tribes=[Tribe.ROYAL]),
            make_character(id="SBB_CHARACTER_COURTWIZARD", position=5)
        ],
    )

    mummy = player.characters[1]
    assert mummy
    unit = player.characters[2]
    assert unit
    prince = enemy.characters[1]
    assert prince
    wizard = enemy.characters[5]
    assert wizard

    fight(player, enemy, limit=1)

    assert mummy.dead
    assert prince.dead
    assert wizard.dead
    assert not unit.dead

    wizardmummy = [
        r for r in wizard._action_history if r.reason == ActionReason.WRETCHED_MUMMY_EXPLOSION
    ]

    assert wizardmummy

def test_courtwizard_noattack_eveniftoken():
    '''This test makes sure that no nonsense occurs like a peep spawning sheep in the court wizar's location
    and then court wizard;'s buff making the sheep attack because the wizard is already dead'''
    player = make_player(
        raw=True,
        characters=[
            make_character(position=1),
            make_character(position=2, health=2)
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    enemy = make_player(
        raw=True,
        characters=[
            make_character(position=1, tribes=[Tribe.ROYAL]),
            make_character(id="SBB_CHARACTER_COURTWIZARD", position=6),
            make_character(id="SBB_CHARACTER_PRINCESSPEEP", position=5)
        ],
    )

    unit = player.characters[1]
    assert unit
    unit2 = player.characters[2]
    assert unit2
    prince = enemy.characters[1]
    assert prince
    wizard = enemy.characters[6]
    assert wizard
    peep = enemy.characters[5]
    assert peep

    class FakeOndeathFallingstars(OnDeath):
        last_breath = False
        def handle(self, *args, **kwargs):
            self.manager.player.cast_spell('SBB_SPELL_FALLINGSTARS')

    unit.register(FakeOndeathFallingstars, priority=9999)

    fight(player, enemy, limit=1)

    assert unit.dead
    assert prince.dead
    assert wizard.dead
    assert peep.dead
    assert not unit2.dead, unit2.pretty_print()

    for pos in [5, 6, 7]:
        assert enemy.characters[pos].id == "SBB_CHARACTER_SHEEP"


def test_courtwizard_ranged():
    player = make_player(
        raw=True,
        characters=[
            make_character(id='SBB_CHARACTER_COURTWIZARD', position=6, attack=3, health=6),
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    enemy = make_player(
        raw=True,
        characters=[make_character(attack=1, health=1)],
    )
    fight(player, enemy, limit=2)

    assert (player.characters[6].attack, player.characters[6].health) == (3, 6)
