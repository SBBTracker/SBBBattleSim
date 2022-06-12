import pytest
from sbbbattlesim import fight
from sbbbattlesim.action import ActionReason
from tests import make_player, make_character

ACTION_COUNTER_TESTS = (
    (
        make_player(characters=[make_character(id='SBB_CHARACTER_POLYWOGGLE')]),
        make_player(characters=[make_character(id='SHEEEEEEEEEEEEEEEEEEEEEP', attack=0)]),
        'Polywoggle Slay',
        1
    ),
    (
        make_player(characters=[make_character(id='SBB_CHARACTER_WRETCHEDMUMMY', attack=0)]),
        make_player(characters=[make_character(id='SHEEEEEEEEEEEEEEEEEEEEEP')]),
        'Wretched Mummy Explosion',
        1
    ),
)


@pytest.mark.parametrize('p1, p2, key, counter', ACTION_COUNTER_TESTS)
def test_stats(p1, p2, key, counter):
    stats = fight(p1, p2)

    for pid, counters in stats.action_counters.items():
        print(pid, counters)

    assert stats.action_counters[p1.id][key] == counter


if __name__ == '__main__':
    for args in ACTION_COUNTER_TESTS:
        test_stats(*args)
