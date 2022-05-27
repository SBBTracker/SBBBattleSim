import pytest

from sbbbattlesim import fight
from sbbbattlesim.action import ActionReason
from tests import make_character, make_player


@pytest.mark.parametrize('golden', (True, False))
def test_baby_root(golden):
    player = make_player(
        raw=True,
        characters=[
            make_character(id="SBB_CHARACTER_BABYROOT", position=5, attack=1, health=1, golden=golden),
            make_character(position=1, attack=1, health=7),
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    enemy = make_player()
    fight(player, enemy, limit=2)

    baby_roof_buff = None
    for action in player.characters[1]._action_history:
        if action.reason == ActionReason.SUPPORT_BUFF:
            baby_roof_buff = action

    assert baby_roof_buff.health == 6 if golden else 3
    baby_roof_buff.roll_back()
    assert player.characters[1].health == (1 if golden else 4)
