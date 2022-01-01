import logging

from sbbbattlesim.characters import registry as character_registry
from sbbbattlesim.heroes import registry as hero_registry
from sbbbattlesim.spells import registry as spell_registry
from sbbbattlesim.treasures import registry as treasure_registry

logger = logging.getLogger(__name__)


def test_character_registry():
    logger.debug(character_registry.items())
    assert character_registry
    assert character_registry.items()


def test_hero_registry():
    logger.debug(hero_registry.items())
    assert hero_registry
    assert hero_registry.items()


def test_spells_registry():
    logger.debug(spell_registry.items())
    assert spell_registry
    assert spell_registry.items()


def test_treasures_registry():
    logger.debug(treasure_registry.items())
    assert treasure_registry
    assert treasure_registry.items()
