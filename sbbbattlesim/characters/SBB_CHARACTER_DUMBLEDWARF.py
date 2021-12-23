import logging

from sbbbattlesim.action import Buff
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnBuff
from sbbbattlesim.utils import Tribe, StatChangeCause

logger = logging.getLogger(__name__)


class DoublyOnBuff(OnBuff):
    def handle(self, reason, stack, attack, health, temp, *args, **kwargs):
        if reason == StatChangeCause.DOUBLEY_BUFF:
            return
        golden_multiplier = 2 if self.doubly.golden else 1
        Buff(reason=StatChangeCause.DOUBLEY_BUFF, source=self.doubly, targets=[self.doubly],
             attack=attack * golden_multiplier, health=health * golden_multiplier, temp=temp, stack=stack).resolve()


# aka doubly
class CharacterType(Character):
    display_name = 'Dubly'

    _attack = 1
    _health = 1
    _level = 3
    _tribes = {Tribe.DWARF}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register(DoublyOnBuff, doubly=self, priority=9999)
