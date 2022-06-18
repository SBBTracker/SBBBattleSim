import pytest
from sbbbattlesim import fight
from sbbbattlesim.action import ActionReason
from tests import make_player, make_character

ACTION_COUNTER_TESTS = (
    (
        make_player(characters=[make_character(id='SBB_CHARACTER_POLYWOGGLE')]),
        make_player(characters=[make_character(id='SHEEEEEEEEEEEEEEEEEEEEEP', attack=0)]),
        'Poly Woggle Slay Chance',
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
        'Wretched Mummy Explosion Damage',
        15
    ),
)


@pytest.mark.parametrize('p1, p2, key, counter', ACTION_COUNTER_TESTS)
def test_stats(p1, p2, key, counter):
    stats = fight(p1, p2)

    for stat_id, counters in stats.adv_stats.items():
        print(stat_id, counters)

    assert stats.adv_stats[p1.id][key] == counter


if __name__ == '__main__':
    for args in ACTION_COUNTER_TESTS:
        test_stats(*args)
