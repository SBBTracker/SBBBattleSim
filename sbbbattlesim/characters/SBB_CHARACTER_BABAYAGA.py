import logging

from sbbbattlesim.action import SupportBuff, EventSupport
from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnSlay
from sbbbattlesim.utils import Tribe

logger = logging.getLogger(__name__)


class BabaYagaOnSlayBuff(OnSlay):
    def handle(self, source, stack, from_yaga=False, *args, **kwargs):
        if isinstance(source, OnSlay) or from_yaga:
            return

        for _ in range(2 if self.baba_yaga.golden else 1):
            with stack.open(source=self, *args, **kwargs) as executor:
                logger.debug(f'Baba Yaga Triggering OnAttackAndKill {source} ({args} {kwargs})')
                executor.execute(source, from_yaga=True, *args, **kwargs)


class BabaYagaSupportBuff(SupportBuff):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.applied_buffs = {}

    def execute(self, character, *args, **kwargs):
        event = character.register(BabaYagaOnSlayBuff, baba_yaga=self.source, temp=True, *args, **kwargs)
        self.applied_buffs[character] = event

    def remove(self):
        for char, buff in self.applied_buffs:
            char.remove(buff)


class CharacterType(Character):
    display_name = 'Baba Yaga'
    support = True
    ranged = True

    _attack = 3
    _health = 6
    _level = 5
    _tribes = {Tribe.EVIL, Tribe.MONSTER}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.support_buff = EventSupport(source=self, event=BabaYagaOnSlayBuff, baba_yaga=self)

    def buff(self, target_character, *args, **kwargs):
        self.support_buff.execute(target_character, *args, **kwargs)
