import pytest

from sbbbattlesim import fight
from sbbbattlesim.utils import Tribe
from tests import make_character, make_player


@pytest.mark.parametrize('golden', (True, False))
def test_wickedwitch(golden):
    player = make_player(
        characters=[
            make_character(id="SBB_CHARACTER_WICKEDWITCHOFTHEWEST", position=5, attack=1, health=1, golden=golden),
            make_character(position=1, attack=1, health=1, tribes=[Tribe.EVIL]),
            make_character(position=2, attack=1, health=1)
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    enemy = make_player()
    fight(player, enemy, limit=0)


    char = player.characters[1]
    buffs = [
        r for r in char._action_history
    ]

    healthbuffs = sum([b.health for b in buffs])
    attackbuffs = sum([b.attack for b in buffs])

    assert attackbuffs == (6 if golden else 3)
    assert healthbuffs == (4 if golden else 2)

    char = player.characters[2]
    buffs = [
        r for r in char._action_history
    ]

    healthbuffs = sum([b.health for b in buffs])
    attackbuffs = sum([b.attack for b in buffs])

    assert attackbuffs == 0
    assert healthbuffs == 0

