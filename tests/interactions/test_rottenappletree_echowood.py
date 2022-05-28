from sbbbattlesim import fight
from tests import make_character, make_player


def test_echowood_rottenappletree():
    player = make_player(
        hero="SBB_HERO_MUERTE",
        characters=[
            make_character(position=2, attack=1, health=100),
            make_character(id="SBB_CHARACTER_ECHOWOODSHAMBLER", position=7, attack=1, health=1),
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    enemy = make_player(
        characters=[
            make_character(id="SBB_CHARACTER_ROTTENAPPLETREE", health=2)
        ],
    )
    fight(player, enemy, limit=1)


    assert (player.characters[7].attack, player.characters[7].health) == (1, 1)
