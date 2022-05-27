import pytest

from sbbbattlesim import fight
from sbbbattlesim.utils import Tribe
from tests import make_character, make_player


@pytest.mark.parametrize("mimic", (True, False))
@pytest.mark.parametrize("n_char", (1, 2))
def test_sarc_phoenix(mimic, n_char):
    characters = []
    for n in range(1, n_char + 1):
        characters.append(make_character(position=n, attack=1, health=1, tribes=[Tribe.EVIL]))

    player = make_player(
        characters=characters,
        treasures=[
            '''SBB_TREASURE_ANCIENTSARCOPHAGUS''',
            "SBB_TREASURE_TREASURECHEST" if mimic else ''
        ]
    )
    enemy = make_player(
        spells=["SBB_SPELL_EARTHQUAKE"],
        characters=[
            make_character(id="SBB_CHARACTER_ECHOWOODSHAMBLER", position=5, attack=1, health=1)
        ],
        treasures=[
            'SBB_TREASURE_PHOENIXFEATHER'
        ]

    )
    fight(player, enemy, limit=2)


    if mimic or n_char > 1:
        assert enemy.characters[5] is None
    else:
        assert enemy.characters[5] is not None
