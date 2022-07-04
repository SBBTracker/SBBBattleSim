import pytest
from sbbbattlesim import fight
from sbbbattlesim.action import ActionReason
from sbbbattlesim.stats import finalize_adv_stats
from tests import make_player, make_character

ACTION_COUNTER_TESTS = (
    (
        make_player(characters=[make_character(id='SBB_CHARACTER_POLYWOGGLE')]),
        make_player(characters=[make_character(id='SHEEEEEEEEEEEEEEEEEEEEEP', attack=0)]),
        'poly_woggle_slay',
        1
    ),
)


@pytest.mark.parametrize('p1, p2, key, counter', ACTION_COUNTER_TESTS)
def test_stats(p1, p2, key, counter):
    stats = fight(p1, p2)

    for stat_id, stat in stats.adv_stats.items():
        print(stat_id, stat)

    assert stats.adv_stats[p1.id][key] == counter
    finalized = finalize_adv_stats([stats])
    print(finalized)


if __name__ == '__main__':
    for args in ACTION_COUNTER_TESTS:
        test_stats(*args)


def test_prized_pig_survival_rate():
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_PRIZEDPIG', health=15),
            make_character(id='SBB_CHARACTER_PRIZEDPIG', health=15, position=2)
        ]
    )
    enemy = make_player(
        characters=[make_character(id='SHEEEEEEEEEEEEEEEEEEEEEP')],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )

    stats = fight(player, enemy)
    assert stats.adv_stats[player.id]['prize_pig_survival_rate'] == 2


def test_prized_pig_survival_rate():
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_PRIZEDPIG', health=15),
            make_character(id='SBB_CHARACTER_PRIZEDPIG', health=15, position=2)
        ]
    )
    enemy = make_player(
        characters=[make_character(id='SHEEEEEEEEEEEEEEEEEEEEEP')],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )

    stats = fight(player, enemy)
    assert stats.adv_stats[player.id]['prize_pig_survival_rate'] == 2


def test_nutcracker_quest_progression():
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_VENGEFULGODMOTHER', health=15, quest_counter=4),
        ]
    )
    enemy = make_player(
        characters=[
            make_character(id='SHEEEEEEEEEEEEEEEEEEEEEP'),
            make_character(id='SHEEEEEEEEEEEEEEEEEEEEEP', position=2),
            make_character(id='SHEEEEEEEEEEEEEEEEEEEEEP', position=3),
            make_character(id='SHEEEEEEEEEEEEEEEEEEEEEP', position=4),
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )

    stats = fight(player, enemy)
    assert stats.adv_stats[player.id]['nutcracker_average_quest_progress'] == 4


def test_brave_princess_slays():
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_QUESTINGPRINCESS', health=15, quest_counter=2),
        ]
    )
    enemy = make_player(
        characters=[
            make_character(id='SHEEEEEEEEEEEEEEEEEEEEEP'),
            make_character(id='SHEEEEEEEEEEEEEEEEEEEEEP', position=2),
            make_character(id='SHEEEEEEEEEEEEEEEEEEEEEP', position=3),
            make_character(id='SHEEEEEEEEEEEEEEEEEEEEEP', position=4),
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )

    stats = fight(player, enemy)
    assert stats.adv_stats[player.id]['brave_princess_average_slays'] == 2


def test_lancelot_quest_completion_chance():
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_LANCELOT', attack=24, health=24, quest_counter=1),
        ]
    )
    enemy = make_player(
        characters=[
            make_character(id='SHEEEEEEEEEEEEEEEEEEEEEP'),
            make_character(id='SHEEEEEEEEEEEEEEEEEEEEEP', position=2),
            make_character(id='SHEEEEEEEEEEEEEEEEEEEEEP', position=3),
            make_character(id='SHEEEEEEEEEEEEEEEEEEEEEP', position=4),
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )

    stats = fight(player, enemy)
    assert stats.adv_stats[player.id]['lancelot_quest_completion_chance'] == 1


def test_hercules_average_damage_done():
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_HERCULES', attack=25, health=5, quest_counter=100),
        ]
    )
    enemy = make_player(
        characters=[
            make_character(id='SHEEEEEEEEEEEEEEEEEEEEEP'),
            make_character(id='SHEEEEEEEEEEEEEEEEEEEEEP', position=2),
            make_character(id='SHEEEEEEEEEEEEEEEEEEEEEP', position=3),
            make_character(id='SHEEEEEEEEEEEEEEEEEEEEEP', position=4),
        ],
        treasures=['''SBB_TREASURE_HERMES'BOOTS''']
    )

    stats = fight(player, enemy)
    assert stats.adv_stats[player.id]['hercules_average_damage_done'] == 100


def test_cinderella_quest_completion():
    player = make_player(
        characters=[
            make_character(id='SBB_CHARACTER_CINDER-ELLA', attack=0, health=5, quest_counter=1, position=5),
            make_character(id='SBB_CHARACTER_MONSTERBOOK', attack=0, health=1, position=1),
        ]
    )
    enemy = make_player(
        characters=[
            make_character(id='SHEEEEEEEEEEEEEEEEEEEEEP'),
        ],
    )

    stats = fight(player, enemy)
    assert stats.adv_stats[player.id]['cinderella_quest_completion_chance'] == 1