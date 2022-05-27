import pytest

from sbbbattlesim import fight
from sbbbattlesim.utils import Tribe
from tests import make_character, make_player


@pytest.mark.parametrize('golden', (True, False))
def test_bossy(golden):
    player = make_player(
        raw=True,
        characters=[
            make_character(id="SBB_CHARACTER_BIGBOSS", position=5, attack=1, health=1, golden=golden),
            make_character(position=6, attack=1, health=1, tribes=[Tribe.DWARF]),
            make_character(position=7, attack=1, health=1)
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    enemy = make_player(raw=True)
    fight(player, enemy, limit=2)

    if golden:
        final_stats = (7, 7)
    else:
        final_stats = (4, 4)

    char = player.characters[6]
    buffs = [
        r for r in char._action_history
    ]

    healthbuffs = sum([b.health for b in buffs])
    attackbuffs = sum([b.attack for b in buffs])

    assert attackbuffs == (6 if golden else 3)
    assert healthbuffs == (6 if golden else 3)

    char = player.characters[7]
    buffs = [
        r for r in char._action_history
    ]

    healthbuffs = sum([b.health for b in buffs])
    attackbuffs = sum([b.attack for b in buffs])

    assert attackbuffs == 0
    assert healthbuffs == 0

