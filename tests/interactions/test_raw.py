import pytest

from sbbbattlesim import fight
from sbbbattlesim.action import ActionReason
from sbbbattlesim.utils import Tribe
from tests import make_character, make_player


@pytest.mark.parametrize('golden', (True, False))
def test_raw_fanny(golden):
    player = make_player(
        raw=True,
        characters=[
            make_character(id="SBB_CHARACTER_ANGRYDWARF",position=5, attack=1, health=1, golden=golden),
            make_character(position=1, attack=5, health=5, tribes=[Tribe.DWARF]),
            make_character(position=2, attack=1, health=1)
        ]
    )
    enemy = make_player(
        characters=[
            make_character(id="SBB_CHARACTER_BABYDRAGON", position=5, attack=1, health=1),
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS''',
        ]
    )
    fight(player, enemy, limit=2)


    if golden:
        final_stats = (1, 1)
    else:
        final_stats = (3, 3)

    assert (player.characters[1].attack, player.characters[1].health) == final_stats
    assert (player.characters[2].attack, player.characters[2].health) == (1, 1)


@pytest.mark.skip(reason='This test does not work after resolve board was removed')
def test_singingswords_bossy():
    player = make_player(
        raw=True,
        characters=[
            make_character(id="SBB_CHARACTER_BIGBOSS", position=5, attack=1, health=1),
            make_character(position=1, attack=6, health=3, tribes=[Tribe.DWARF]),
        ],
        treasures=[
            "SBB_TREASURE_WHIRLINGBLADES",
        ]
    )
    enemy = make_player()
    fight(player, enemy, limit=1)

    char = player.characters[1]
    assert (char.attack, char.health) == (6, 3)

    singing_sword_aura = False
    bossy_aura = False
    for action in char._action_history:
        if action.reason == ActionReason.SINGINGSWORD_BUFF:
            singing_sword_aura = True
        if action.reason == ActionReason.BOSSY_BUFF:
            bossy_aura = True

    assert singing_sword_aura
    assert bossy_aura