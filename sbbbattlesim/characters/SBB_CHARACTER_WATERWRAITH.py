import logging

from sbbbattlesim.action import Buff, Aura, ActionReason
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnDeath
from sbbbattlesim.utils import Tribe, get_adjacent_targets

logger = logging.getLogger(__name__)


class WaterWraithOnDeath(OnDeath):
    last_breath = False

    def handle(self, stack, *args, **kwargs):
        modifier = 2 if self.source.golden else 1

        Buff(source=self.source, reason=ActionReason.WATER_WRAITH_BUFF, targets=[self.source],
             health=modifier, attack=modifier, temp=False, stack=stack).resolve()


class CharacterType(Character):
    display_name = 'Water Wraith'

    _attack = 2
    _health = 2
    _level = 3
    _tribes = {Tribe.EVIL, Tribe.MONSTER}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.aura = Aura(source=self, event=WaterWraithOnDeath, _lambda=lambda char: char.position in get_adjacent_targets(self.position))
