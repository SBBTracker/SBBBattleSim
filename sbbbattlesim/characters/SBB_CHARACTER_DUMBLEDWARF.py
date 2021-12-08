import logging

from sbbbattlesim.action import Buff
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnBuff
from sbbbattlesim.utils import Tribe, StatChangeCause

logger = logging.getLogger(__name__)


class DoublyOnBuff(OnBuff):
    def handle(self, *args, **kwargs):
        Buff(reason=StatChangeCause.DOUBLEY_BUFF, source=self.doubly, targets=[self.doubly], *args, **kwargs)


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
