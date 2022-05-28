from sbbbattlesim import fight
from sbbbattlesim.utils import Tribe
from tests import make_character, make_player


def test_courtwizard_spearofachilles():
    player = make_player(
        characters=[
            make_character(position=1),
            make_character(position=2)
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    enemy = make_player(
        characters=[
            make_character(position=1, tribes=[Tribe.ROYAL]),
            make_character(id="SBB_CHARACTER_COURTWIZARD", position=5)
        ],
        treasures=['''SBB_TREASURE_SPEAROFACHILLES''']
    )
    fight(player, enemy, limit=1)


    assert (enemy.characters[5].attack, enemy.characters[5].health) == (8, 8)
