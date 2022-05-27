import pytest

from sbbbattlesim import fight
from sbbbattlesim.utils import Tribe
from tests import make_character, make_player


@pytest.mark.parametrize('golden', (True, False))
@pytest.mark.parametrize('limit', (0, 1, 2))
def test_oni(golden, limit):
    player = make_player(
        characters=[
            make_character(
                id='SBB_CHARACTER_MONSTERLORD', position=6, attack=1, health=1,
                golden=golden, tribes=[Tribe.MONSTER]
            ),
            make_character(
                position=1, attack=1, health=1, tribes=[Tribe.MONSTER]
            ),
            make_character(
                position=2, attack=1, health=1,
            ),
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    enemy = make_player(
        characters=[
            make_character(attack=0, health=1, position=1),
            make_character(attack=0, health=1, position=2),
            make_character(attack=0, health=1, position=3),
        ],
    )
    fight(player, enemy, limit=limit)


    final_stats = (21, 21) if golden else (11, 11)

    assert player.characters[1].attack, player.characters[1].health == final_stats
    assert player.characters[2].attack, player.characters[2].health == (1, 1)
    if limit >= 2:
        assert player.characters[6].attack, player.characters[6].health == final_stats
    else:
        assert player.characters[6].attack, player.characters[6].health == (1, 1)
