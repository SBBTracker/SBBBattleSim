from sbbbattlesim import fight
from tests import make_character, make_player


def test_phoenix_cupid():
    player = make_player(
        characters=[
            make_character(position=1, attack=1, health=500),
            make_character(position=5, attack=500, health=1),
        ],
        treasures=['SBB_TREASURE_PHOENIXFEATHER']
    )
    enemy = make_player(
        characters=[make_character(id="SBB_CHARACTER_CUPID", attack=1, health=1)],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    fight(player, enemy, limit=1)


    assert player.characters[1] is None
    assert player.characters[5] is None


def test_phoenix_bouncy_cupid():
    player = make_player(
        characters=[
            make_character(id="SBB_CHARACTER_CUPID", position=5, attack=1, health=500),
            make_character(position=1, attack=500, health=1),
        ],
        treasures=['SBB_TREASURE_PHOENIXFEATHER']
    )
    enemy = make_player(
        characters=[make_character(id="SBB_CHARACTER_CUPID", attack=1, health=1)],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )
    fight(player, enemy, limit=1)


    assert player.characters[1] is None
    assert player.characters[5] is None
