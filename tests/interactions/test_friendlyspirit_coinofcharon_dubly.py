import pytest

from sbbbattlesim import fight
from sbbbattlesim.utils import Tribe
from tests import make_character, make_player


@pytest.mark.parametrize('golden', (True, False))
def test_friendlyspirit_coinofcharon_dubly(golden):
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_FRIENDLYGHOST', position=1, attack=5, health=5, golden=golden),
            make_character(id='SBB_CHARACTER_DUMBLEDWARF', position=5, attack=1, health=1, golden=golden),
        ],
        treasures=['''SBB_TREASURE_MONKEY'SPAW''']
    )
    enemy = make_player(
        characters=[
            make_character(attack=5, health=5),
            make_character(position=7, attack=0, health=3)
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    fight(player, enemy, limit=-1)


    if golden:
        final_stats = (55, 55)
    else:
        final_stats = (19, 19)

    assert (player.characters[5].attack, player.characters[5].health) == final_stats


def test_friendlyspirit_monstermanual():
    '''Manual should go off before friendly spirit'''
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_FRIENDLYGHOST', position=1, attack=5, health=5, tribes=[Tribe.MONSTER]),
            make_character(position=5, attack=1, health=1),
        ],
        treasures=['''SBB_TREASURE_MONSTERMANUAL''']
    )
    enemy = make_player(
        characters=[
            make_character(attack=5, health=5),
            make_character(position=7, attack=0, health=3)
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    fight(player, enemy, limit=-1)


    assert (player.characters[5].attack, player.characters[5].health) == (8, 6)
