from sbbbattlesim import fight
from sbbbattlesim.action import ActionReason, ActionState
from tests import make_character, make_player


def test_rotten_appletree():
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_ROTTENAPPLETREE', position=6, attack=0, health=5),
        ]
    )
    enemy = make_player(
        characters=[
            make_character(attack=1, health=1000, position=1),
        ]
    )
    fight(player, enemy, limit=2)


    assert enemy.characters[1].health == 1


def test_rotten_appletree_support():
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_ROTTENAPPLETREE', position=1, attack=0, health=5),
        ]
    )
    enemy = make_player(
        characters=[
            make_character(attack=1, health=1000, position=1),
            make_character(id="SBB_CHARACTER_BABYROOT", attack=1, health=1000, position=5)
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    fight(player, enemy, limit=1)


    assert enemy.characters[1].health == 1


def test_rotten_appletree_health_support_dies():
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_ROTTENAPPLETREE', position=1, attack=0, health=5),
            make_character(id='SBB_CHARACTER_BABYDRAGON', position=6, attack=3, health=3),
        ]
    )
    enemy = make_player(
        characters=[
            make_character(attack=1, health=1000, position=1),
            make_character(id="SBB_CHARACTER_BABYROOT", attack=1, health=1, position=5)
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    frontchar = enemy.characters[1]
    backchar = enemy.characters[5]
    fight(player, enemy, limit=2)

    assert backchar.dead
    assert frontchar.dead

    baby_root_buff = None
    for action in frontchar._action_history:
        if action.reason == ActionReason.SUPPORT_BUFF and action.health == 3:
            baby_root_buff = action

    assert baby_root_buff
    assert baby_root_buff.state == ActionState.ROLLED_BACK


def test_rotten_appletree_attack_support_dies():
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_ROTTENAPPLETREE', position=1, attack=0, health=5),
            make_character(id='SBB_CHARACTER_BABYDRAGON', position=5, attack=3, health=3),
        ]
    )
    enemy = make_player(
        characters=[
            make_character(attack=1, health=1000, position=1),
            make_character(id="SBB_CHARACTER_MADMADAMMIM", attack=1, health=1, position=5)
        ],
        treasures=[
            '''SBB_TREASURE_HERMES'BOOTS'''
        ]
    )
    frontchar = enemy.characters[1]
    backchar = enemy.characters[5]
    fight(player, enemy, limit=2)

    assert frontchar.health == 1
    assert backchar.dead
