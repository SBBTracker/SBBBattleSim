import logging

from sbbbattlesim.action import Buff, ActionReason
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnBuff
from sbbbattlesim.utils import Tribe

logger = logging.getLogger(__name__)


class DoublyOnBuff(OnBuff):
    def handle(self, reason, stack, attack, health, *args, **kwargs):
        if reason in [ActionReason.DOUBLEY_BUFF, ActionReason.SINGINGSWORD_BUFF]:
            return
        golden_multiplier = 2 if self.source.golden else 1
        Buff(reason=ActionReason.DOUBLEY_BUFF, source=self.source, targets=[self.source],
             attack=attack * golden_multiplier, health=health * golden_multiplier, stack=stack).resolve()


# aka doubly
class CharacterType(Character):
    display_name = 'Dubly'

    _attack = 2
    _health = 2
    _level = 3
    _tribes = {Tribe.DWARF}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(DoublyOnBuff, priority=9999)
