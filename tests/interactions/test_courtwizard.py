import pytest

from sbbbattlesim import Board
from sbbbattlesim.utils import Tribe
from sbbbattlesim.action import ActionReason
from tests import make_character, make_player
from sbbbattlesim.events import OnDeath


@pytest.mark.parametrize('tribe', (Tribe.ROYAL, Tribe.ROYAL, Tribe.DWARF))
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
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=1)

    if tribe in [Tribe.ROYAL, Tribe.ROYAL]:
        assert board.p1.characters[1] is None and board.p1.characters[2] is None


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
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    mummy = board.p1.characters[1]
    assert mummy
    unit = board.p1.characters[2]
    assert unit
    prince = board.p2.characters[1]
    assert prince
    wizard = board.p2.characters[5]
    assert wizard

    winner, loser = board.fight(limit=1)


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
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    unit = board.p1.characters[1]
    assert unit
    unit2 = board.p1.characters[2]
    assert unit2
    prince = board.p2.characters[1]
    assert prince
    wizard = board.p2.characters[6]
    assert wizard
    peep = board.p2.characters[5]
    assert peep

    class FakeOndeathFallingstars(OnDeath):
        last_breath = False
        def handle(self, *args, **kwargs):
            self.manager.player.cast_spell('SBB_SPELL_FALLINGSTARS')

    unit.register(FakeOndeathFallingstars, priority=9999)

    winner, loser = board.fight(limit=1)



    assert unit.dead
    assert prince.dead
    assert wizard.dead
    assert peep.dead
    assert not unit2.dead, unit2.pretty_print()

    for pos in [5, 6, 7]:
        assert board.p2.characters[pos].id == "SBB_CHARACTER_SHEEP"

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
    board = Board({'PLAYER': player, 'ENEMY': enemy})
    winner, loser = board.fight(limit=2)


    assert (board.p1.characters[6].attack, board.p1.characters[6].health) == (3, 6)
