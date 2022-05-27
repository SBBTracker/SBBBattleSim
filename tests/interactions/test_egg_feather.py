from sbbbattlesim import fight
from tests import make_character, make_player



def test_egg_feather():
    player = make_player(
        raw=True,
        treasures=['''SBB_TREASURE_PHOENIXFEATHER'''],
        characters=[
            make_character(
                id="SBB_CHARACTER_HUMPTYDUMPTY",position=1, attack=1, health=1,
                golden=False
            ),
        ],
    )
    enemy = make_player(
        raw=True,
        characters=[
            make_character(position=1, attack=1, health=1),
         ],

    )
    fight(player, enemy, limit=2)

    assert player.characters[1] is None
