from sbbbattlesim import fight
from tests import make_character, make_player


def test_negative_attack():
    player = make_player(
        characters=[
            make_character(),
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    enemy = make_player(
        characters=[
            make_character(attack=-100)
        ],
    )
    fight(player, enemy, limit=1)


    assert (player.characters[1].attack, player.characters[1].health) == (1, 1)
