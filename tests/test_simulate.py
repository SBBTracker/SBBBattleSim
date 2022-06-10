import typing

import pytest
from attr import dataclass

from sbbbattlesim.simulate import simulate_brawl, simulate
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


@dataclass
class MockLogObject:
    zone: str = ''
    content_id: str = ''

    cardattack: str = ''
    cardhealth: str = ''
    is_golden: bool = ''
    cost: str = '0'
    slot: str = '0'
    subtypes: typing.List[str] = []

    level: str = '0'

    counter: str = '0'


STATE_DATA = (
    {
        'Player 1 ID HERE': [
            MockLogObject(
                zone='Character',
                content_id='SBB_CHARACTER_BLACKCAT',
                cardattack='4',
                cardhealth='4',
                is_golden=True,
                cost='2',
                slot='0',  # This is to make sure it does the proper correction
                subtypes=['evil', 'animal']
            ),
            MockLogObject(
                zone='Treasure',
                content_id='SBB_TREASURE_ANCIENTSARCOPHAGUS',
            ),
            MockLogObject(
                zone='Hero',
                content_id='SBB_HERO_DRACULA',
            ),
            MockLogObject(
                zone='Spell',
                content_id='SBB_SPELL_BEASTWITHIN',
            ),
            MockLogObject(
                zone='Hand',
                content_id='SBB_CHARACTER_LEAPFROG',
                cardattack='4',
                cardhealth='4',
                is_golden=True,
                cost='2',
                slot='15',  # This will not matter as position will be set if it moves to the board
                subtypes=['good', 'monster']
            ),
        ],
        'Other Player ID Goes Here': [
            MockLogObject(
                zone='Character',
                content_id='SBB_CHARACTER_NIGHTSTALKER',
                cardattack='2',
                cardhealth='2',
                is_golden=True,
                cost='2',
                slot='0',  # This is to make sure it does the proper correction
                subtypes=['evil', 'monster']
            ),
            MockLogObject(
                zone='Character',
                content_id='SBB_CHARACTER_BABYROOT',
                cardattack='0',
                cardhealth='6',
                is_golden=False,
                cost='2',
                slot='4',  # This is to make sure it does the proper correction
                subtypes=['good', 'treant']
            ),
            MockLogObject(
                zone='Hero',
                content_id='SBB_HERO_GANDALF',
            ),
        ]
    },
)


@pytest.mark.parametrize('data', STATE_DATA)
def test_simulate(data):
    simulate(data)