import sys

import pytest

from sbbbattlesim import fight
from tests import make_player, make_character


@pytest.mark.skipif('benchmark' not in sys.argv, reason='Only used for benchmarking')
def test_tedious():
    import time
    t = time.perf_counter()
    for _ in range(1):

        player = make_player(
            characters=[
                make_character(id='SBB_CHARACTER_RIVERWISHMERMAID', position=5, attack=5, health=5, golden=False),
                make_character(id='SBB_CHARACTER_BABAYAGA', position=6, attack=3, health=6, golden=True),
                make_character(id='SBB_CHARACTER_BABAYAGA', position=7, attack=3, health=6, golden=True),
                make_character(id="SBB_CHARACTER_SHADOWASSASSIN", position=1, attack= 1, health=100),
                make_character(id="SBB_CHARACTER_SHADOWASSASSIN", position=2, attack=1, health=100),
                make_character(id="SBB_CHARACTER_SHADOWASSASSIN", position=3, attack=1, health=100),
                make_character(id="SBB_CHARACTER_SHADOWASSASSIN", position=4, attack=1, health=100),
            ],
            treasures=[
                'SBB_TREASURE_HELMOFCOMMAND',
                'SBB_TREASURE_TREASURECHEST',
                '''SBB_TREASURE_BANNEROFCOMMAND'''
            ]
        )
        enemy = make_player(
            characters=[
                make_character(id="SBB_CHARACTER_BABYBEAR", attack=0, health=1, position=1),
                make_character(id="SBB_CHARACTER_BABYBEAR", attack=0, health=1, position=2),
                make_character(id="SBB_CHARACTER_BABYBEAR", attack=0, health=1, position=3),
                make_character(id="SBB_CHARACTER_BABYBEAR", attack=0, health=1, position=4),
                make_character(id="SBB_CHARACTER_BABYBEAR", attack=0, health=1, position=5),
                make_character(id="SBB_CHARACTER_BABYBEAR", attack=0, health=1, position=6),
                make_character(id="SBB_CHARACTER_BABYBEAR", attack=0, health=1, position=7),
            ],
        )

        fight(player, enemy)

    raise ValueError(time.perf_counter() - t)