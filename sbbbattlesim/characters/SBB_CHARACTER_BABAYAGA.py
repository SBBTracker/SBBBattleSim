from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnSlay
from sbbbattlesim.utils import StatChangeCause, Tribe
import logging

logger = logging.getLogger(__name__)

class CharacterType(Character):
    display_name = 'Baba Yaga'
    support = True

    _attack = 3
    _health = 6
    _level = 5
    _tribes = {Tribe.EVIL, Tribe.MONSTER}

    def buff(self, target_character):

        # NOTE: this is so HUGELY fragile based on fundamental changes to the event manager
        # frankly if you can't fix this while updating the event manager then you shouldn't change either
        class BabaYagaOnSlayBuff(OnSlay):
            baba_yaga = self
            def handle(self, source, *args, **kwargs):
                if isinstance(source, BabaYagaOnSlayBuff):
                    return

                for _ in range(2 if self.baba_yaga.golden else 1):
                    reaction = source(*args, **kwargs, source=source)
                    if reaction:
                        react, evt_args, evt_kwargs = reaction

                        logger.info(f'Baba Yaga Event Manager handling: {react} reacting to {self} with source={self} ({evt_args} {evt_kwargs})')
                        self.manager(react, *evt_args, **evt_kwargs, source=self)

        target_character.register(BabaYagaOnSlayBuff, temp=True)
