import pytest

from sbbbattlesim.simulate import simulate_brawl
from tests import PLAYER, make_character

SIM_DATA = (
    {
        'PLAYER_ID': PLAYER | {
            'characters': [make_character()]
        },
        'ENEMY_ID': PLAYER | {
            'characters': [make_character()]
        }
    },

)


@pytest.mark.parametrize('data', SIM_DATA)
def test_simulate_brawl(data):
    simulate_brawl(data, k=1)