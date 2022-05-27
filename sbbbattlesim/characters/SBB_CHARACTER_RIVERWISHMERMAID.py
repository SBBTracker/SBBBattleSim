import logging

from sbbbattlesim import utils
from sbbbattlesim.action import Buff, Support, ActionReason
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnAttackAndKill, OnSpawn
from sbbbattlesim.utils import Tribe

logger = logging.getLogger(__name__)


class RiverwishMermaidOnAttackAndKill(OnAttackAndKill):
    slay = True

    def handle(self, killed_character, stack, *args, **kwargs):
        stats = 2 if self.source.golden else 1
        Buff(reason=ActionReason.SUPPORT_BUFF, source=self.source, targets=[self.manager], attack=stats, health=stats,
             stack=stack).resolve()


class RiverWishOnSpawn(OnSpawn):
    def handle(self, stack, *args, **kwargs):
        player = self.source.player
        if 'SBB_TREASURE_CLOAKOFTHEASSASSIN' in player.treasures:
            target_positions = utils.get_support_targets(self.source.position, player.banner_of_command)
            logger.debug(target_positions)
            targets = player.valid_characters(_lambda=lambda char: char.position in target_positions)
            logger.debug(targets)

            for cloak in player.treasures['SBB_TREASURE_CLOAKOFTHEASSASSIN']:
                cloak.aura.execute(*targets)


class CharacterType(Character):
    display_name = 'Riverwish Mermaid'
    support = True

    _attack = 4
    _health = 8
    _level = 4
    _tribes = {Tribe.GOOD, Tribe.ROYAL}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(RiverWishOnSpawn)
        self.support = Support(source=self, event=RiverwishMermaidOnAttackAndKill, priority=100)


