import logging

from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnSlay
from sbbbattlesim.utils import Tribe

logger = logging.getLogger(__name__)

class CharacterType(Character):
    display_name = 'Baba Yaga'
    support = True
    ranged = True

    _attack = 3
    _health = 6
    _level = 5
    _tribes = {Tribe.EVIL, Tribe.MONSTER}

    def buff(self, target_character, *args, **kwargs):
        class BabaYagaOnSlayBuff(OnSlay):
            baba_yaga = self

            def handle(self, source, stack, *args, **kwargs):
                if isinstance(source, OnSlay):
                    return

                for _ in range(2 if self.baba_yaga.golden else 1):
                    with stack.open(source=self, *args, **kwargs) as executor:
                        logger.debug(f'Baba Yaga Triggering OnAttackAndKill {source} ({args} {kwargs})')
                        executor.execute(source, *args, **kwargs)

        target_character.register(BabaYagaOnSlayBuff, temp=True)
