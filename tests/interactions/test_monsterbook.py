import pytest

from sbbbattlesim import fight
from sbbbattlesim.action import ActionReason
from sbbbattlesim.utils import Tribe
from tests import make_character, make_player


@pytest.mark.parametrize('golden', (True, False))
def test_monsterbook_wizard_familar(golden):
    player = make_player(
        level=2,
        characters=[
            make_character(id='SBB_CHARACTER_MONSTERBOOK', position=1, attack=1, health=1, golden=golden),
            make_character(id='''SBB_CHARACTER_WIZARD'SFAMILIAR''', position=2, attack=1, health=5),
            make_character(id='''SBB_CHARACTER_WIZARD'SFAMILIAR''', position=3, attack=1, health=5),
            make_character(id='''SBB_CHARACTER_WIZARD'SFAMILIAR''', position=4, attack=1, health=5),
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    enemy = make_player(
        characters=[make_character(attack=1, health=1)],
    )
    fight(player, enemy, limit=1)


    for pos in [2, 3, 4]:
        wizardbuffs = [
            r for r in player.characters[pos]._action_history if r.reason == ActionReason.WIZARDS_FAMILIAR
        ]

        assert len(wizardbuffs) == (2 if golden else 1)


@pytest.mark.parametrize('golden', (True, False))
def test_monsterbook_spellweaver(golden):
    player = make_player(
        level=2,
        characters=[
            make_character(id='SBB_CHARACTER_MONSTERBOOK', position=1, attack=1, health=1, golden=golden),
            make_character(id='SBB_CHARACTER_TIM', position=2, attack=1, health=5),
            make_character(id='SBB_CHARACTER_TIM', position=3, attack=1, health=5),
            make_character(id='SBB_CHARACTER_TIM', position=4, attack=1, health=5),
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    enemy = make_player(
        characters=[make_character(attack=1, health=1)],
    )
    fight(player, enemy, limit=1)


    for pos in [2, 3, 4]:
        wizardbuffs = [
            r for r in player.characters[pos]._action_history if r.reason == ActionReason.SPELL_WEAVER
        ]

        assert len(wizardbuffs) == (2 if golden else 1)


@pytest.mark.parametrize('golden', (True, False))
def test_monsterbook_aon(golden):

    player = make_player(
        level=2,
        characters=[
            make_character(id='SBB_CHARACTER_MONSTERBOOK', position=1, attack=1, health=1, golden=golden),
            make_character(id='SBB_CHARACTER_SUMMONER', position=2, attack=1, health=5, tribes={Tribe.MAGE}),
            make_character(id='SBB_CHARACTER_SUMMONER', position=3, attack=1, health=5),
            make_character(id='SBB_CHARACTER_SUMMONER', position=4, attack=1, health=5, tribes={Tribe.MAGE})
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    enemy = make_player(
        characters=[make_character(attack=1, health=1)],
    )
    fight(player, enemy, limit=1)


    for pos in [2, 3, 4]:
        wizardbuffs = [
            r for r in player.characters[pos]._action_history if r.reason == ActionReason.AON_BUFF
        ]

        num_buffs = (6 if golden else 3)
        if pos == 3:
            num_buffs = 0

        assert len(wizardbuffs) == num_buffs

