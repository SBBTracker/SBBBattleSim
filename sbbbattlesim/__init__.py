import logging

logger = logging.getLogger(__name__)


from sbbbattlesim.combat import fight
from sbbbattlesim.config import configure_logging
from sbbbattlesim.simulate import simulate, from_state
from sbbbattlesim.exceptions import SBBBSCrocException

from sbbbattlesim.heroes import registry as hero_registry
from sbbbattlesim.spells import registry as spell_registry
from sbbbattlesim.treasures import registry as treasure_registry
from sbbbattlesim.characters import registry as character_registry

hero_registry.autoregister()
spell_registry.autoregister()
treasure_registry.autoregister()
character_registry.autoregister()
