import pytest

from sbbbattlesim import simulate
from sbbbattlesim.simulate import _process

sim_data = [
    {'717fdd43-e7d8-426e-8eb1-ef9edb9930a4': {'characters': [{'id': 'SBB_CHARACTER_CATBURGLAR', 'attack': 1, 'health': 1, 'golden': True, 'cost': 2, 'position': 1, 'tribes': ['evil', 'animal'], 'raw': True}, {'id': 'SBB_CHARACTER_ANGRYDWARF', 'attack': 2, 'health': 2, 'golden': True, 'cost': 2, 'position': 7, 'tribes': ['dwarf'], 'raw': True}, {'id': 'SBB_CHARACTER_WEEWILLIEWINKIE', 'attack': 8, 'health': 3, 'golden': True, 'cost': 2, 'position': 3, 'tribes': ['dwarf'], 'raw': True}], 'treasures': [], 'hero': None, 'spells': ['SBB_SPELL_FORBIDDENFRUIT'], 'level': 0, 'hand': []}, 'D2AEBB2B532D4F5B': {'characters': [{'id': 'SBB_CHARACTER_BLINDMOUSE', 'attack': 2, 'health': 2, 'golden': True, 'cost': 2, 'position': 1, 'tribes': ['animal'], 'raw': True}, {'id': 'SBB_CHARACTER_FRIENDLYTREE', 'attack': 2, 'health': 2, 'golden': True, 'cost': 2, 'position': 2, 'tribes': ['good', 'treant'], 'raw': True}], 'treasures': [], 'hero': None, 'spells': ['SBB_SPELL_SUGARANDSPICE'], 'level': 0, 'hand': []}},
]


@pytest.mark.parametrize('data', sim_data)
def test_multiprocessing(data):
    _process(data, 1, 1)
