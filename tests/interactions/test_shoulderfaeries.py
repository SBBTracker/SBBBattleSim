from sbbbattlesim import fight
from sbbbattlesim.utils import Tribe
from tests import make_character, make_player


def test_shoulderfaeries():
    player = make_player(
        characters=[
            make_character(
                id="SBB_CHARACTER_GOODANDEVILSISTERS", position=1, attack=1, health=1
            ),
            make_character(position=6, attack=1000, health=100, tribes=[Tribe.GOOD]),
            make_character(position=5, attack=100, health=1000, tribes=[Tribe.EVIL]),
        ],
        treasures=[
            'SBB_TREASURE_MIRRORUNIVERSE'
        ],
    )
    enemy = make_player(
        characters=[
            make_character(position=1, attack=200, health=200),
        ],
    )

    fight(player, enemy, limit=1)

    final_stats = (100, 100)

    assert (player.characters[1].attack, player.characters[1].health) == final_stats

