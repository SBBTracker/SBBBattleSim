import pytest

from sbbbattlesim import fight
from sbbbattlesim.utils import Tribe
from tests import make_character, make_player


@pytest.mark.parametrize('arthur_is_golden', (True, False))
def test_prince_arthur(arthur_is_golden):
    player = make_player(
        characters=[
            make_character(
                id="SBB_CHARACTER_KINGARTHUR", position=5,
                attack=1, health=1, golden=arthur_is_golden, tribes=[Tribe.ROYAL]
            ),
            make_character(position=1, attack=1, health=1, tribes=[Tribe.ROYAL]),
            make_character(position=2, attack=1, health=1, tribes=[Tribe.ROYAL], golden=True),
            make_character(position=3, attack=1, health=1, tribes=[Tribe.ROYAL]),
            make_character(position=4, attack=1, health=1, tribes=[Tribe.ROYAL], golden=True),
            make_character(position=6, attack=1, health=1, golden=True),
        ],
    )
    enemy = make_player()
    fight(player, enemy, limit=0)


    if arthur_is_golden:
        golden_final_stats = (5, 5)
    else:
        golden_final_stats = (3, 3)
    normal_stats = (1, 1)

    assert (player.characters[1].attack, player.characters[1].health) == normal_stats
    assert (player.characters[2].attack, player.characters[2].health) == golden_final_stats
    assert (player.characters[3].attack, player.characters[3].health) == normal_stats
    assert (player.characters[4].attack, player.characters[4].health) == golden_final_stats
    assert (player.characters[5].attack, player.characters[5].health) == (
        golden_final_stats if arthur_is_golden else normal_stats)
    assert (player.characters[6].attack, player.characters[6].health) == normal_stats
