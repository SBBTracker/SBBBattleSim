from sbbbattlesim import fight
from sbbbattlesim.action import ActionReason
from sbbbattlesim.utils import Tribe
from tests import make_character, make_player


def test_raw_doubly():
    player = make_player(
        raw=True,
        characters=[
            make_character(id='SBB_CHARACTER_DUMBLEDWARF', position=1, attack=5, health=5, tribes=[Tribe.DWARF]),
            make_character(id='SBB_CHARACTER_ANGRYDWARF', position=5, attack=5, health=5),
        ],
    )
    enemy = make_player()
    fight(player, enemy, limit=0)

    dubly = player.characters[1]
    angry_buff = None
    for action in dubly._action_history:
        if action.reason == ActionReason.SUPPORT_BUFF:
            angry_buff = action
            break

    assert angry_buff
    assert angry_buff.attack == 2
    assert angry_buff.health == 2

    assert dubly.attack == 5
    assert dubly.health == 5
    angry_buff.roll_back()
    assert dubly.attack == 1
    assert dubly.health == 1