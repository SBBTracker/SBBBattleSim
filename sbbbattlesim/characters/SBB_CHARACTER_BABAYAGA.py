import logging

from sbbbattlesim.action import Support
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnSlay
from sbbbattlesim.utils import Tribe

logger = logging.getLogger(__name__)


class BabaYagaOnSlayBuff(OnSlay):
    def handle(self, source, stack, *args, **kwargs):
        if isinstance(source, OnSlay):
            return

        for _ in range(2 if self.source.golden else 1):
            with stack.open(source=self, *args, **kwargs) as executor:
                logger.debug(f'Baba Yaga Triggering OnAttackAndKill {source} ({args} {kwargs})')
                executor.execute(source, *args, **kwargs)


class CharacterType(Character):
    display_name = 'Baba Yaga'
    support = True
    ranged = True

    _attack = 3
    _health = 6
    _level = 5
    _tribes = {Tribe.EVIL, Tribe.MONSTER, Tribe.MAGE}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.support = Support(source=self, attack=6 if self.golden else 3, event=BabaYagaOnSlayBuff)
