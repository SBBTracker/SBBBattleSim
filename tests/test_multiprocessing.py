import sys

import pytest

from sbbbattlesim.characters import registry as character_registry
from sbbbattlesim.heroes import registry as hero_registry
from sbbbattlesim.simulate import _process
from sbbbattlesim.spells import registry as spell_registry
from sbbbattlesim.treasures import registry as treasure_registry
from tests import make_character, make_player

sim_data = [
    {'717fdd43-e7d8-426e-8eb1-ef9edb9930a4': {'characters': [{'id': 'SBB_CHARACTER_CATBURGLAR', 'attack': 1, 'health': 1, 'golden': True, 'cost': 2, 'position': 1, 'tribes': ['evil', 'animal'], 'raw': True}, {'id': 'SBB_CHARACTER_ANGRYDWARF', 'attack': 2, 'health': 2, 'golden': True, 'cost': 2, 'position': 7, 'tribes': ['dwarf'], 'raw': True}, {'id': 'SBB_CHARACTER_WEEWILLIEWINKIE', 'attack': 8, 'health': 3, 'golden': True, 'cost': 2, 'position': 3, 'tribes': ['dwarf'], 'raw': True}], 'treasures': [], 'hero': None, 'spells': ['SBB_SPELL_FORBIDDENFRUIT'], 'level': 0, 'hand': []}, 'D2AEBB2B532D4F5B': {'characters': [{'id': 'SBB_CHARACTER_BLINDMOUSE', 'attack': 2, 'health': 2, 'golden': True, 'cost': 2, 'position': 1, 'tribes': ['animal'], 'raw': True}, {'id': 'SBB_CHARACTER_FRIENDLYTREE', 'attack': 2, 'health': 2, 'golden': True, 'cost': 2, 'position': 2, 'tribes': ['good', 'treant'], 'raw': True}], 'treasures': [], 'hero': None, 'spells': ['SBB_SPELL_SUGARANDSPICE'], 'level': 0, 'hand': []}},
]


@pytest.mark.skipif('processing' not in sys.argv, reason='Not Including Multiprocessing Tests')
@pytest.mark.parametrize('data', sim_data)
def test_multiprocessing(data):
    _process(data, 1, 1)


@pytest.mark.skipif('processing' not in sys.argv, reason='Not Including Multiprocessing Tests')
@pytest.mark.parametrize('char', character_registry.filter())
def test_character_pickling(char):
    '''Run a combat, results dont matter. This will either crash or pass'''
    data = {
        'Player': make_player(
            characters=[make_character(id=char.id)],
        ),
        'Enemy': make_player()
    }
    _process(data, 1, 1)


@pytest.mark.skipif('processing' not in sys.argv, reason='Not Including Multiprocessing Tests')
@pytest.mark.parametrize('hero', hero_registry.filter())
def test_hero_pickling(hero):
    '''Run a combat, results dont matter. This will either crash or pass'''
    data = {
        'Player': make_player(
            hero=hero,
        ),
        'Enemy': make_player()
    }
    _process(data, 1, 1)


@pytest.mark.skipif('processing' not in sys.argv, reason='Not Including Multiprocessing Tests')
@pytest.mark.parametrize('treasure', treasure_registry.filter())
def test_treasure_pickling(treasure):
    '''Run a combat, results dont matter. This will either crash or pass'''
    data = {
        'Player': make_player(
            treasures=[treasure],
        ),
        'Enemy': make_player()
    }
    _process(data, 1, 1)


@pytest.mark.skipif('processing' not in sys.argv, reason='Not Including Multiprocessing Tests')
@pytest.mark.parametrize('spell', spell_registry.filter())
def test_spell_pickling(spell):
    '''Run a combat, results dont matter. This will either crash or pass'''
    data = {
        'Player': make_player(
            spells=[spell],
        ),
        'Enemy': make_player()
    }
    _process(data, 1, 1)