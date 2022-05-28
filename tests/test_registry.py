import logging

import pytest

from sbbbattlesim.characters import registry as character_registry
from sbbbattlesim.heroes import registry as hero_registry
from sbbbattlesim.spells import registry as spell_registry
from sbbbattlesim.treasures import registry as treasure_registry

logger = logging.getLogger(__name__)


@pytest.mark.parametrize('registry', (character_registry, hero_registry, spell_registry, treasure_registry))
def test_registry(registry):
    logger.debug(registry.items())
    assert registry
    assert registry.items()
    assert len(registry.items()) > 0
