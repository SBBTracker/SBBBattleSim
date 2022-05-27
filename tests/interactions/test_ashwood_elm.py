import pytest

from sbbbattlesim import fight
from sbbbattlesim.utils import Tribe
from tests import make_character, make_player


@pytest.mark.parametrize('golden', (True, False))
def test_ashwood_elm(golden):
    player = make_player(
        raw=True,
        characters=[
            make_character(
                id="SBB_CHARACTER_KINGTREE", position=5,
                attack=1, health=100, golden=golden, tribes=[Tribe.TREANT]
            ),
            make_character(position=1, attack=1, health=1, tribes=[Tribe.TREANT]),
            make_character(position=2, attack=1, health=1),
        ],
    )
    enemy = make_player(raw=True)
    fight(player, enemy, limit=0)

    treant_attack = (201 if golden else 101)

    assert (player.characters[1].attack, player.characters[1].health) == (treant_attack, 1)
    assert (player.characters[2].attack, player.characters[2].health) == (1, 1)
    assert (player.characters[5].attack, player.characters[5].health) == (treant_attack, 100)
