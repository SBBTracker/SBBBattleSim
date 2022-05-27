import pytest

from sbbbattlesim import fight
from sbbbattlesim.utils import Tribe
from tests import make_character, make_player


@pytest.mark.parametrize('golden', (True, False))
def test_rainbow_unicorn(golden):
    player = make_player(
        characters=[
            make_character(
                id="SBB_CHARACTER_HELPFULGODMOTHER", position=5, attack=1,
                health=1, golden=golden, tribes=[Tribe.GOOD]
            ),
            make_character(position=6, attack=1, health=1, tribes=[Tribe.GOOD]),
            make_character(position=7, attack=1, health=1)
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    enemy = make_player()
    fight(player, enemy, limit=0)


    if golden:
        final_stats = (1, 3)
    else:
        final_stats = (1, 2)

    char = player.characters[5]
    buffs = [
        r for r in char._action_history
    ]

    healthbuffs = sum([b.health for b in buffs])
    attackbuffs = sum([b.attack for b in buffs])

    assert attackbuffs == 0
    assert healthbuffs == 0

    char = player.characters[6]
    buffs = [
        r for r in char._action_history
    ]

    healthbuffs = sum([b.health for b in buffs])
    attackbuffs = sum([b.attack for b in buffs])

    assert attackbuffs == 0
    assert healthbuffs == (2 if golden else 1)

    char = player.characters[7]
    buffs = [
        r for r in char._action_history
    ]

    healthbuffs = sum([b.health for b in buffs])
    attackbuffs = sum([b.attack for b in buffs])

    assert attackbuffs == 0
    assert healthbuffs == 0

