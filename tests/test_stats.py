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
    (
        make_player(characters=[make_character(id='SBB_CHARACTER_WRETCHEDMUMMY', attack=15)]),
        make_player(
            characters=[
                make_character(id='SHEEEEEEEEEEEEEEEEEEEEEP'),
                make_character(id='SHEEEEEEEEEEEEEEEEEEEEEP', position=2)
            ],
            treasures=['''SBB_TREASURE_HERMES'BOOTS''']
        ),
        'wretched_mummy_explosion_damage',
        15
    ),
    (
        make_player(
            characters=[
                make_character(id='SBB_CHARACTER_PRIZEDPIG', health=15),
                make_character(id='SBB_CHARACTER_PRIZEDPIG', health=15, position=2)
            ]
        ),
        make_player(characters=[make_character(id='SHEEEEEEEEEEEEEEEEEEEEEP')], treasures=['''SBB_TREASURE_HERMES'BOOTS''']),
        'prize_pig_survival_rate',
        2
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
