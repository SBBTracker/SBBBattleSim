import pytest
from tests import fight_monstar, make_character, make_player
from sbbbattlesim.characters import registry as character_registry

@pytest.mark.parametrize('attack', (True, False))
@pytest.mark.parametrize('golden', (True, False))
@pytest.mark.parametrize('char', character_registry.characters.keys())
def test_character(char, attack, golden):
    char = make_character(id=char, golden=golden)
    player = make_player([char], treasures=['''SBB_TREASURE_HERMES'BOOTS'''] if attack else [])
    fight_monstar(player)