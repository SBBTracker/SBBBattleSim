import logging

from sbbbattlesim.board import Board
from sbbbattlesim.characters import registry as character_registry
from sbbbattlesim.config import configure_logging
from sbbbattlesim.heros import registry as hero_registry
from sbbbattlesim.simulate import simulate
from sbbbattlesim.spells import registry as spell_registry
from sbbbattlesim.treasures import registry as treasure_registry
from sbbbattlesim.exceptions import SBBBSCrocException

SUMMONING_PRIORITY = 10


logger = logging.getLogger(__name__)


def setup():
    configure_logging()
    character_registry.autoregister()
    hero_registry.autoregister()
    spell_registry.autoregister()
    treasure_registry.autoregister()


setup()
