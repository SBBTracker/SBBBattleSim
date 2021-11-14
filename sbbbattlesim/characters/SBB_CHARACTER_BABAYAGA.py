from sbbbattlesim.characters import Character
from sbbbattlesim.events import OnSlay
from sbbbattlesim.utils import StatChangeCause, Tribe


class CharacterType(Character):
    display_name = 'Baba Yaga'
    support = True

    _attack = 3
    _health = 6
    _level = 5
    _tribes = {Tribe.EVIL, Tribe.MONSTER}

    def buff(self, target_character):

        class BabaYagaOnSlayBuff(OnSlay):
            baba_yaga = self
            def handle(self, source, *args, **kwargs):
                for _ in range(2 if self.baba_yaga.golden else 1):
                    source(*args, **kwargs)

        target_character.register(BabaYagaOnSlayBuff, temp=True)
